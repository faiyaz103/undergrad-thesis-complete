"""
XGBoost baseline for the adaptive-decryption risk classifier.

Protocol (identical to the deployed random forest):
  - same 8-element feature vector (one-hot role, ordinal sensitivity, pass-through counts)
  - same stratified 70/15/15 partitions, fitted on the training partition only
  - hyperparameters selected on the VALIDATION partition
  - the TEST partition is scored exactly once, with the selected configuration

Balanced and unbalanced variants are both searched, mirroring the ClassBalancer check
run against the Weka baselines, so the row is a tuned baseline rather than a strawman.

Reference: T. Chen and C. Guestrin, "XGBoost: A Scalable Tree Boosting System,"
Proc. 22nd ACM SIGKDD, 2016, pp. 785-794. doi:10.1145/2939672.2939785

Usage:  pip install xgboost
        python xgboost_pipeline.py
"""

import os
import json
import pandas as pd
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                             f1_score, precision_recall_fscore_support)
from sklearn.utils.class_weight import compute_sample_weight
from xgboost import XGBClassifier
import xgboost

# --------------------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------------------
DATASET_DIR = r'f:\ICCIT26\adaptive-data-access-framework-dataset-and-model\dataset'
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = 42

GRID = {
    'n_estimators':  [100, 300],
    'max_depth':     [3, 6],
    'learning_rate': [0.05, 0.1, 0.3],
}
BALANCING = [True, False]

# Deployed random forest, quarantined test partition -- printed for reference only.
RF_REFERENCE = {
    'accuracy': 0.9780, 'weighted_f1': 0.9777, 'macro_f1': 0.9407,
    'medium_f1': 0.8929, 'low_pass': 0.9914, 'high_intercept': 0.9281,
}

CLASS_NAMES = ['LOW (full decrypt)', 'MEDIUM (partial mask)', 'HIGH (deny)']


# --------------------------------------------------------------------------------------
# Feature mapping -- must stay identical to the training pipeline and the TypeScript
# runtime. Any reordering silently corrupts every prediction.
# --------------------------------------------------------------------------------------
def preprocess_to_numeric(df):
    X = pd.DataFrame()
    X['role_customer']        = (df['user_role'] == 'customer').astype(int)   # x[0]
    X['role_moderator']       = (df['user_role'] == 'moderator').astype(int)  # x[1]
    X['role_admin']           = (df['user_role'] == 'admin').astype(int)      # x[2]
    X['resource_sensitivity'] = df['resource_sensitivity'].map(
        {'LOW': 0, 'MEDIUM': 1, 'HIGH': 2}).astype(int)                       # x[3]
    X['is_office_hours']      = df['is_office_hours'].astype(int)             # x[4]
    X['record_owner_match']   = df['record_owner_match'].astype(int)          # x[5]
    X['recent_request_count'] = df['recent_request_count'].astype(int)        # x[6]
    X['failed_attempt_count'] = df['failed_attempt_count'].astype(int)        # x[7]
    return X


def load_partition(name):
    df = pd.read_csv(os.path.join(DATASET_DIR, f'access_logs_{name}.csv'))
    return preprocess_to_numeric(df), df['risk_level']


def evaluate(y_true, y_pred):
    """Aggregate scores plus the two security-operational readings of the matrix."""
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1, 2])
    _, _, f1_per_class, _ = precision_recall_fscore_support(
        y_true, y_pred, labels=[0, 1, 2], zero_division=0)
    return {
        'accuracy':       accuracy_score(y_true, y_pred),
        'weighted_f1':    f1_score(y_true, y_pred, average='weighted', zero_division=0),
        'macro_f1':       f1_score(y_true, y_pred, average='macro', zero_division=0),
        'medium_f1':      f1_per_class[1],
        'low_pass':       cm[0, 0] / cm[0].sum(),   # legitimate requests served in full
        'high_intercept': cm[2, 2] / cm[2].sum(),   # high-risk contexts refused outright
        'confusion':      cm,
    }


def build(params):
    return XGBClassifier(tree_method='hist', random_state=SEED, n_jobs=-1,
                         eval_metric='mlogloss', **params)


# --------------------------------------------------------------------------------------
# 1. Load
# --------------------------------------------------------------------------------------
print(f'xgboost {xgboost.__version__}\n')

X_train, y_train = load_partition('train')
X_val,   y_val   = load_partition('val')
X_test,  y_test  = load_partition('test')

print(f'train {len(X_train)}   val {len(X_val)}   test {len(X_test)}')
print('test class counts', y_test.value_counts().sort_index().to_dict(), '\n')

# Multi-class analogue of class_weight='balanced'. NOTE: scale_pos_weight is binary-only
# and does nothing here -- weighting must go through sample_weight.
sample_weight_balanced = compute_sample_weight('balanced', y_train)


# --------------------------------------------------------------------------------------
# 2. Hyperparameter search -- VALIDATION partition only
# --------------------------------------------------------------------------------------
print('=' * 80)
print('Grid search (validation partition)')
print('=' * 80)

results = []
for balanced in BALANCING:
    sw = sample_weight_balanced if balanced else None
    for n in GRID['n_estimators']:
        for d in GRID['max_depth']:
            for lr in GRID['learning_rate']:
                params = {'n_estimators': n, 'max_depth': d, 'learning_rate': lr}
                model = build(params).fit(X_train, y_train, sample_weight=sw)
                m = evaluate(y_val, model.predict(X_val))
                results.append({'params': params, 'balanced': balanced, **m})
                print(f'  bal={str(balanced):5s} n={n:<4d} d={d} lr={lr:<5}'
                      f' -> wF1 {m["weighted_f1"]:.4f}  macroF1 {m["macro_f1"]:.4f}'
                      f'  MED-F1 {m["medium_f1"]:.4f}  HIGH-rec {m["high_intercept"]:.4f}')

best = max(results, key=lambda r: r['weighted_f1'])
print(f'\nSelected on validation weighted F1: {best["params"]} '
      f'balanced={best["balanced"]} -> {best["weighted_f1"]:.4f}\n')


# --------------------------------------------------------------------------------------
# 3. Single test-set evaluation
# --------------------------------------------------------------------------------------
print('=' * 80)
print('Final evaluation (quarantined test partition -- scored once)')
print('=' * 80)

final_sw = sample_weight_balanced if best['balanced'] else None
final_model = build(best['params']).fit(X_train, y_train, sample_weight=final_sw)
test_pred = final_model.predict(X_test)
test = evaluate(y_test, test_pred)

print(classification_report(y_test, test_pred, target_names=CLASS_NAMES,
                            digits=4, zero_division=0))
print('Confusion matrix (rows actual, cols predicted):')
print(pd.DataFrame(test['confusion'],
                   index=['actual LOW', 'actual MED', 'actual HIGH'],
                   columns=['pred LOW', 'pred MED', 'pred HIGH']))

print(f'\n{"metric":<22}{"XGBoost":>10}{"RandomForest":>14}{"delta":>10}')
for k in ['accuracy', 'weighted_f1', 'macro_f1', 'medium_f1', 'low_pass', 'high_intercept']:
    print(f'{k:<22}{test[k]:>10.4f}{RF_REFERENCE[k]:>14.4f}{test[k] - RF_REFERENCE[k]:>+10.4f}')

print(f'\nHigh-risk contexts receiving full plaintext: '
      f'{test["confusion"][2][0]} of {test["confusion"][2].sum()}   '
      f'(random forest: 9 of 139)')

print('\nFeature importance (gain):')
for name, imp in sorted(zip(X_train.columns, final_model.feature_importances_),
                        key=lambda t: -t[1]):
    print(f'  {name:<24}{imp:.4f}')


# --------------------------------------------------------------------------------------
# 4. Persist
# --------------------------------------------------------------------------------------
summary = {
    'xgboost_version': xgboost.__version__,
    'selected_params': best['params'],
    'balanced': best['balanced'],
    'validation_weighted_f1': round(float(best['weighted_f1']), 4),
    'grid_searched': {**GRID, 'sample_weight_balanced': BALANCING},
    'configurations_evaluated': len(results),
    'test': {k: round(float(test[k]), 4) for k in
             ['accuracy', 'weighted_f1', 'macro_f1', 'medium_f1', 'low_pass', 'high_intercept']},
    'test_confusion_matrix': test['confusion'].tolist(),
}
out_json = os.path.join(OUT_DIR, 'xgboost_results.json')
with open(out_json, 'w', encoding='utf-8') as fh:
    json.dump(summary, fh, indent=2)

# Paper-ready row, 3 dp to match the cross-model comparison table.
t = summary['test']
print('\nLaTeX row for the cross-model table:')
print(f'XGBoost ($n{{=}}{best["params"]["n_estimators"]}$, $d{{=}}{best["params"]["max_depth"]}$)'
      f' & Python & {t["weighted_f1"]:.3f} & {t["macro_f1"]:.3f} & {t["medium_f1"]:.3f}'
      f' & {t["low_pass"]*100:.2f}\\% & {t["high_intercept"]*100:.2f}\\% \\\\')
print(f'\nwrote {out_json}')
