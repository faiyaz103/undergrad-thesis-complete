# Part D — RBF-kernel SVM

Weka's built-in SVM is `SMO` (sequential minimal optimisation). Nothing to install. Its multi-class strategy is pairwise one-vs-one, which matches scikit-learn's `SVC`, so this is a fair comparison.

## D1. Load and configure

Load `access_logs_train_numeric8.arff` in **Preprocess**, then **Classify** tab → **Supplied test set** → **Set...** → `access_logs_val_numeric8.arff` (validation for now — you're tuning).

**Choose** → `functions` → **SMO**. Click the options text box to open the editor:

- `c` = **1.0** to start (this is the complexity/regularisation constant, sklearn's `C`)
- `filterType` = **Normalize training data** (the default; leave it — SVMs are scale-sensitive and this is Weka's equivalent of your `StandardScaler` step)
- `kernel` → click it → **Choose** → **RBFKernel** → set `gamma` = **0.01** (Weka's default)

Click **OK**, then **Start**.

## D2. Tune C and gamma on validation

This step is not optional. Weka's default `gamma = 0.01` and scikit-learn's `gamma='scale'` are very different values, so a single default run tells you nothing about whether RBF SVMs suit this problem.

Run this grid, recording validation weighted F-measure for each of the nine combinations:

- `c` ∈ {1, 10, 100}
- `gamma` ∈ {0.01, 0.1, 0.5}

⚠️ **Watch the `-C` collision:** **SMO's** `c` is the complexity constant, but **RBFKernel's** `-C` is the kernel cache size. In the GUI they're in separate editors so you can't mix them up; on the command line, be careful which one you're setting.

Expect this to be slow — SMO on 7,000 instances with an RBF kernel and high `C` can take minutes per run, and high `C` values are the slowest. Nine runs is a coffee break, not a click.

## D3. Final run

Take the best `(c, gamma)` by **validation** weighted F-measure, switch the supplied test set to `access_logs_test_numeric8.arff`, and run once. That number is your table row.

## D4. What to expect

An RBF SVM draws smooth curved boundaries, whereas your labels come from axis-aligned threshold conjunctions (`v > 15`, `f ≥ 5`). I'd expect it to land clearly above the linear models but below the tree ensembles. If it does, that's a genuinely useful result for your paper: it separates "non-linearity helps" from "*rule-shaped* non-linearity helps," and only the tree ensembles deliver the second. That distinction currently isn't evidenced anywhere in your draft.

Also record its **HIGH recall** specifically. SMO has no `class_weight='balanced'` equivalent, so it will likely under-serve your minority classes — worth a sentence.

---

# Part E — AdaBoost

Weka's is `AdaBoostM1`, also built in.

## E1. Configure

**Choose** → `meta` → **AdaBoostM1**. Open the editor:

- `classifier` → **Choose** → `trees` → **DecisionStump** (this is AdaBoost's classic base learner and matches scikit-learn's default depth-1 tree)
- `numIterations` = **50** (Weka defaults to 10, scikit-learn to 50 — use 50 for comparability)
- `seed` = **42**

Leave `useResampling` off and `weightThreshold` at 100.

## E2. Tune iterations on validation

Try `numIterations` ∈ {10, 50, 100, 200} against the validation file. Boosting can overfit with too many rounds, and you want to show you checked rather than accepting a default.

If stumps plateau early, try swapping the base classifier to `trees.J48` or a depth-3 `REPTree` — a stump can only test one feature at a time, which is a poor fit for labels defined by 3–4 term conjunctions.

## E3. A real caveat to watch for

`AdaBoostM1` is the original two-class formulation, adapted for multi-class. It **halts early** if the base learner's weighted error reaches 0.5, and with three imbalanced classes this happens more readily than you'd expect. Check the output header for how many iterations actually ran — if it says far fewer than you requested, AdaBoost stopped early and the row is a legitimate finding, not a misconfiguration. Say so in the paper rather than quietly tuning around it. Scikit-learn's `AdaBoostClassifier` uses SAMME, which handles multi-class more gracefully, so a gap between the two implementations here is expected and explainable.

## E4. Final run

Best iteration count by validation → switch to the test file → one run.

---

# Part F — XGBoost

Here's the honest situation: **XGBoost does not ship with Weka**, and I can't confirm from memory whether a maintained XGBoost package exists in the package manager for your version. Check for yourself:

**Weka GUI Chooser** → **Tools** → **Package Manager** → search for `XGBoost`, then `boost`, then `gradient`. Install anything relevant, then restart Weka (packages don't load until restart).

You have three paths, in descending order of how much I'd recommend them:

## F1. Best available: LogitBoost (built in, no install)

`LogitBoost` is Weka's native additive-logistic-regression boosting — genuinely the same algorithmic family as gradient boosting, and it's in core Weka. This gives you a real boosted-ensemble row from an independent implementation, which is the actual point of the exercise.

**Choose** → `meta` → **LogitBoost**:

- `classifier` → `trees` → **DecisionStump** (or `REPTree` with `maxDepth` 3 for more capacity)
- `numIterations` = **100**
- `shrinkage` = **1.0**, then try **0.1** — this is the learning-rate analogue, and 0.1 with more iterations is the configuration that usually behaves like XGBoost's defaults
- `seed` = **42**

Tune `numIterations` × `shrinkage` on validation, then one test run. Label the row **LogitBoost**, not XGBoost.

## F2. If a package exists

Use it, configure `numIterations`/`maxDepth`/`learningRate` analogously, tune on validation, report as a Weka result.

## F3. What not to do

The `wekaPython` package exposes `ScikitLearnClassifier`, which can reach scikit-learn and XGBoost from inside the Weka GUI. It will run, and the number will be real — but it is **not an independent implementation cross-check**. It's your Python stack in a Weka wrapper, so it cannot serve the purpose you added Weka for. If you go this route, or if you simply run XGBoost directly in Python, label that row's source explicitly as Python in the table. A table that silently mixes Weka and Python results under one heading is the kind of thing that unravels badly under review.

---

# Recording results

For each of the three final runs, copy down: accuracy, weighted-average F-measure, macro F-measure (average the three per-class F-measures yourself — Weka doesn't print it), class `0` recall (your LOW pass rate), class `2` recall (your HIGH interception rate), and the full confusion matrix. Also note the tuned hyperparameters, since the paper needs them for reproducibility.
