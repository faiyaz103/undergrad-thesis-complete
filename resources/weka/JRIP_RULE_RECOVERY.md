# JRip (RIPPER) rule recovery — result record and assessment

**Status:** Runs A, B1 and B2 complete. Seed-stability check and training-partition noise rate outstanding.
**Date:** 2026-08-29
**Purpose:** Originally not a baseline — this run existed to test whether a rule-induction algorithm can reconstruct the synthetic labelling policy, i.e. whether classification performance on this corpus measures *policy recovery* rather than *attack detection*. It answered that question, and produced a second result that materially affects how the paper must be framed.

---

## 0. Summary of what the three runs say

1. **The labelling policy is almost fully recoverable.** JRip recovers 5 of 11 generator rules verbatim — including all four numeric thresholds exactly — and 5 more in generalised or fragmented form. Only the rarest rule is missed.
2. **The recovery generalises.** Train 98.31% → test 98.00%, a gap of 0.31 pp. The rule list is not a memorisation artefact.
3. **JRip is at the corpus ceiling.** 30 test errors against 27 test rows carrying unlearnable redrawn labels. Roughly three genuine mistakes in 1,500.
4. **JRip outperforms the deployed random forest on the held-out test partition, on every reported metric**, including both security-operational ones.
5. **Encoding is irrelevant to JRip.** Natural nominal and `numeric8` give identical accuracy (98.00%) and near-identical per-class figures.

Consequence: the paper can no longer claim the random forest is the best-performing model on this corpus. It can, and should, claim that the corpus is saturated by any model family able to represent axis-aligned conjunctions — which is a stronger and more defensible position. See §6.

---

## 1. Configuration

| Item | Value |
|---|---|
| Classifier | `weka.classifiers.rules.JRip -F 3 -N 2.0 -O 2 -S 42` |
| Training data | 7,000 rows, both encodings |
| Rules induced | 14 (13 conditions + 1 default) |
| Build time | 0.26–0.40 s |

| Run | Encoding | Test mode | Purpose |
|---|---|---|---|
| **A** | natural nominal | training set | read the rule list |
| **B1** | natural nominal | supplied test set | generalisation of *that* rule list; ceiling check |
| **B2** | `numeric8` | supplied test set | comparison-table row, on equal footing with other models |

**Encoding note.** Run A used the natural nominal encoding so that JRip emits `(user_role = customer)` rather than `(role_customer >= 1)`, making the rules directly comparable to the generator. B2 repeats on `numeric8` for consistency with SMO, AdaBoost, and the forest. B1 and B2 turned out to be equivalent in performance, so this disclosure is now a formality rather than a caveat.

**B1 confirmed the rule list is byte-identical to Run A**, which licenses comparing the two runs' scores as train-versus-test on one model.

---

## 2. Induced rule list (verbatim, Runs A and B1)

```
(record_owner_match = 0) and (user_role = customer) and (resource_sensitivity = LOW)
    and (recent_request_count <= 6) and (failed_attempt_count <= 4) => risk_level=1 (133.0/3.0)
(recent_request_count >= 9) and (recent_request_count <= 15) and (record_owner_match = 1)
    and (failed_attempt_count <= 4) => risk_level=1 (102.0/5.0)
(record_owner_match = 0) and (is_office_hours = 0) and (resource_sensitivity = MEDIUM)
    and (user_role = moderator) => risk_level=1 (59.0/8.0)
(user_role = admin) and (recent_request_count >= 20) => risk_level=1 (23.0/1.0)
(recent_request_count >= 7) and (resource_sensitivity = LOW) and (record_owner_match = 0)
    and (user_role = customer) and (recent_request_count <= 9) => risk_level=1 (19.0/4.0)
(user_role = moderator) and (record_owner_match = 1)
    and (recent_request_count >= 25) => risk_level=1 (11.0/1.0)
(is_office_hours = 0) and (user_role = moderator)
    and (resource_sensitivity = MEDIUM) => risk_level=1 (14.0/0.0)
(user_role = admin) and (failed_attempt_count >= 3)
    and (failed_attempt_count <= 4) => risk_level=1 (9.0/0.0)
(user_role = moderator) and (recent_request_count >= 22)
    and (recent_request_count <= 25) => risk_level=1 (4.0/1.0)
(recent_request_count >= 16) => risk_level=2 (301.0/10.0)
(failed_attempt_count >= 5) => risk_level=2 (131.0/3.0)
(record_owner_match = 0) and (user_role = customer) => risk_level=2 (105.0/5.0)
(resource_sensitivity = HIGH) and (user_role = moderator) => risk_level=2 (105.0/6.0)
 => risk_level=0 (5984.0/71.0)
```

Parenthesised numbers are `(instances covered / misclassified)` on the training partition.

---

## 3. Results

### 3.1 Run A — training partition (diagnostic only, not reportable)

Accuracy 98.3143%, Kappa 0.9358, weighted F 0.983.
Confusion: `[[5913, 13, 16], [49, 351, 8], [22, 10, 618]]`

| Class | Precision | Recall | F |
|---|---|---|---|
| LOW | 0.988 | 0.995 | 0.992 |
| MEDIUM | 0.939 | 0.860 | 0.898 |
| HIGH | 0.963 | 0.951 | 0.957 |

### 3.2 Run B1 — natural encoding, quarantined test partition

Accuracy **98.00%** (1470/1500), Kappa 0.9235, weighted F **0.980**, macro F **0.945**.
Confusion: `[[1265, 3, 6], [11, 75, 1], [8, 1, 130]]`

| Class | Precision | Recall | F |
|---|---|---|---|
| LOW | 0.985 | 0.993 | 0.989 |
| MEDIUM | 0.949 | 0.862 | 0.904 |
| HIGH | 0.949 | 0.935 | 0.942 |

LOW pass rate 1265/1274 = **99.29%**; HIGH interception 130/139 = **93.53%**.

### 3.3 Run B2 — `numeric8`, quarantined test partition

Accuracy **98.00%** (1470/1500), Kappa 0.9232, weighted F **0.980**, macro F **0.945**.
Confusion: `[[1266, 2, 6], [11, 74, 2], [9, 0, 130]]`

| Class | Precision | Recall | F |
|---|---|---|---|
| LOW | 0.984 | 0.994 | 0.989 |
| MEDIUM | 0.974 | 0.851 | 0.908 |
| HIGH | 0.942 | 0.935 | 0.939 |

LOW pass rate 1266/1274 = **99.37%**; HIGH interception 130/139 = **93.53%**.

### 3.4 Against the deployed random forest (same test partition)

| Metric | Random forest | JRip (B1) | JRip (B2) | Δ (B1 − RF) |
|---|---|---|---|---|
| Accuracy | 0.9780 | **0.9800** | **0.9800** | +0.0020 |
| Weighted F1 | 0.9777 | **0.980** | **0.980** | +0.0023 |
| Macro F1 | 0.9407 | **0.945** | **0.945** | +0.0043 |
| MEDIUM F1 | 0.8929 | **0.904** | **0.908** | +0.0111 |
| MEDIUM recall | 0.8621 | 0.8621 | 0.8506 | 0.0000 |
| LOW pass | 99.14% | **99.29%** | **99.37%** | +0.15 pp |
| HIGH interception | 92.81% | **93.53%** | **93.53%** | +0.72 pp |
| Total test errors | 33 | **30** | **30** | −3 |

**JRip equals or beats the forest on every reported metric.** Its MEDIUM advantage is precision (0.949 vs 0.9259), not recall — recall is identical at 0.8621. It intercepts 130 of 139 high-risk contexts against the forest's 129.

---

## 4. Recovery scorecard

| # | Generator rule | JRip's version | Verdict |
|---|---|---|---|
| 3 | moderator ∧ sens = HIGH | `(sens=HIGH) and (moderator) => 2` | **verbatim** |
| 6 | any ∧ f ≥ 5 | `(f >= 5) => 2` | **verbatim** |
| 8 | customer ∧ 9 ≤ v ≤ 15 | `(v>=9) and (v<=15) and (owner=1) and (f<=4) => 1` | **verbatim interval** |
| 9 | moderator ∧ ¬hours ∧ sens = MED | `(office=0) and (moderator) and (sens=MEDIUM) => 1` | **verbatim** |
| 10 | admin ∧ f ∈ {3,4} | `(admin) and (f>=3) and (f<=4) => 1` | **verbatim** |
| 1 | customer ∧ ¬owner ∧ sens ∈ {MED,HIGH} | `(owner=0) and (customer) => 2` | generalised |
| 2 | customer ∧ v > 15 | `(v >= 16) => 2` | generalised |
| 4 | moderator ∧ v > 25 ∧ ¬owner | fall-through to `(v >= 16) => 2` | recovered by ordering |
| 7 | customer ∧ ¬owner ∧ sens = LOW | split across rules 1 and 5 | fragmented |
| 11 | (mod ∨ admin) ∧ v > 18 | split across three role-specific rules | fragmented |
| 5 | admin ∧ ¬hours ∧ sens=HIGH ∧ v>20 | — | **not recovered** |

**5 of 11 verbatim; 10 of 11 recovered in some form.**

Rule 5 requires admin (5%) ∧ off-hours (20%) ∧ HIGH sensitivity (10%) ∧ high velocity simultaneously — a handful of rows at most, correctly discarded by pruning.

### Two secondary observations

**Role asymmetry recovered through ordering, not through role tests.** Rule 12 is `(owner=0) and (customer) => 2` with the sensitivity condition dropped — it can be, because the LOW-sensitivity cases are caught by rules 1 and 5 earlier in the list. Likewise `(v >= 16) => 2` carries no role condition, because staff-tier velocity cases are pre-empted by the `admin ∧ v>=20` and `moderator ∧ 22–25` rules above it. JRip found a shorter *equivalent decision list*, exploiting the same first-match-wins semantics the generator uses.

**Every recovered threshold is exact.** `v >= 16` ≡ `v > 15`; `9 <= v <= 15` is the MEDIUM band verbatim; `f >= 5` and `f ∈ [3,4]` are exact. This is the fifth independent recovery of the generator's cutoffs across four algorithms and two toolkits (random-forest root split at 15.5; AdaBoost stumps at 8.5 and 4.5; the boosted REPTree conjunction; JRip).

---

## 5. The corpus ceiling — now measurable

27 of the 1,500 test rows (1.80%) carry a 4%-redraw label contradicting the generator's own rules; they are unlearnable by construction. That places the ceiling at approximately **98.2%**.

JRip's test accuracy is **98.00%**, with **30 errors**. Since ~27 of those rows cannot be classified correctly by any model that has learned the policy, this is consistent with roughly **three genuine errors in 1,500**.

The train→test gap is **0.31 pp** (98.31% → 98.00%), which rules out the earlier concern that the rule list was fitted to training noise. It generalises.

⚠️ Two qualifications remain:
1. The claim "≈3 genuine errors" is an inference from the arithmetic (30 errors, 27 unlearnable rows), not a verified row-by-row overlap. The two sets have not been intersected.
2. The 1.80% figure is measured on the test partition — correct for this comparison, but the training-partition rate is still unmeasured and the Run A discussion should not rely on it.

---

## 6. What this means for the paper

The rule-recovery finding was expected. The performance finding was not, and it changes what the paper may claim.

### The claim that must go

Any statement that the random forest is the best-performing model on this corpus. It isn't. A 14-rule decision list, readable in full on half a page, beats it on accuracy, weighted F1, macro F1, MEDIUM F1, legitimate pass rate, and high-risk interception simultaneously.

Omitting this row from the comparison table is not an option. A reviewer can reproduce it in ten minutes, and a baseline that beats the proposed model, discovered after publication, is far more damaging than one disclosed by the authors.

### The claim that gets stronger

The evidence across all models now forms a clean pattern:

| Can represent axis-aligned conjunctions | Cannot |
|---|---|
| JRip 0.980, Random forest 0.978, Decision tree 0.973 | AdaBoost+stumps 0.856, RBF SVM ≈0.96 (MEDIUM recall 0.57–0.63), Logistic regression 0.821 |

Every model that can express `role ∧ interval ∧ ownership` reaches the corpus ceiling; every model that cannot fails specifically on the MEDIUM tier. That is a sharper and better-evidenced claim than "our forest scored highest," and it is exactly the argument Section III-D currently makes without evidence.

### The honest justification for deploying the forest

Not accuracy. On this corpus there is no accuracy argument, and attempting one will not survive scrutiny. What remains, in order of strength:

1. **The synthetic corpus is a bootstrap, not the deployment target.** The rules were recovered from labels a rule engine produced. No such oracle exists behind real access telemetry, and on production data the question of which model family wins is open. A rule learner is guaranteed to do well precisely here and nowhere in particular else.
2. **The graduated policy requires `P(c | x)`.** Tier boundaries, the audit record's probability estimates, and any cost-matrix or threshold calibration all need calibrated class probabilities. A decision list emits a label.
3. **Retraining is the designed path.** The Layer-8 audit tables accumulate telemetry in the training-feature schema specifically so the model can be re-estimated. That path assumes a learned estimator, not a hand-maintained rule set.

Argument 1 is the load-bearing one and should be stated first.

### The reframing this supports

The paper already says the classifier is a replaceable component and the contribution is the late-binding enforcement architecture. This result is now direct evidence for that position rather than an awkward concession. Lean into it.

---

## 7. How solid is it?

**Solid:** the rule recovery, the ceiling comparison, and the performance comparison.
**Still open:** seed stability.

### Firm

- **Deterministic and reproducible.** Fixed seed, fixed data, commands recorded in §9.
- **Directly verifiable.** The rules can be checked against `dataset/script.py` by any reader; no statistical inference involved.
- **Large effect on thresholds.** Exact matches on four separate cutoffs do not arise by chance.
- **Independently corroborated.** Four other algorithms across two toolkits recovered the same boundaries.
- **The generalisation claim now holds.** B1's 0.31 pp train→test gap resolves the earlier training-set-evaluation objection.
- **The performance comparison is like-for-like.** Same partitions, same single evaluation, and encoding-independent (B1 ≡ B2).

### Remaining weaknesses

1. **Single seed.** JRip's pruning uses a random fold split (`-F 3 -S 42`). The rule list, and hence the recovery count, may vary across seeds. *Fix: repeat with seeds 1, 7, 123, 2024 and report whether the count and the four thresholds are stable, or report the range.*
2. **The scorecard involves judgment.** "Verbatim" is objective; "recovered by ordering" and "fragmented" are interpretive, and a skeptical reader could score rules 4 and 11 differently. *Fix: lead with the conservative figure — **5 verbatim, including all four numeric thresholds exactly** — and present 10-of-11 as elaboration with the reasoning shown.*
3. **The "≈3 genuine errors" inference** is arithmetic, not a verified intersection of the two row sets. *Fix: intersect JRip's misclassified test rows with the 27 rule-inconsistent rows, or state it as "consistent with" rather than "equal to".*
4. **Margins are small.** +0.002 accuracy is 3 rows out of 1,500. Do not describe JRip as decisively better — describe both as at the ceiling, which is the accurate reading and also the more useful one.

---

## 8. Draft text for the paper

Placement: one row in the cross-model comparison table, plus a paragraph in Section VI. The rule list is a verbatim listing or figure.

```latex
A rule-induction baseline (RIPPER) was applied under the identical protocol. It recovers
five of the eleven labelling rules verbatim---including all four numeric thresholds
exactly, among them the \MED{} band $9 \le v \le 15$---and five more in generalised or
fragmented form, expressing the role asymmetry through rule ordering rather than explicit
role conditions. Only the rarest rule, requiring four simultaneous conditions, is not
recovered. On the held-out partition the resulting 14-rule decision list reaches 0.980
weighted F1 and 0.945 macro F1, marginally above the selected forest, with 30 test errors
against the 27 rows whose labels the 4\% redraw made inconsistent with the generator.

Both models are therefore at the corpus ceiling, and the comparison across all evaluated
models resolves along a single axis: every model able to represent axis-aligned
conjunctions---rule list, single tree, forest---reaches it, while linear models, an RBF
kernel and boosted stumps fail specifically on the \MED{} tier. This is the clearest
available evidence for the representational argument of Section~III-D. It is equally
clear evidence that performance on this corpus measures recovery of the synthetic
labelling policy rather than detection of attacker behaviour: the rules were recovered
from labels a rule engine produced, and no such oracle exists behind real access
telemetry.

The framework accordingly treats the risk model as an interchangeable component. The
forest is retained because the graduated policy consumes calibrated class probabilities,
which a decision list does not provide, and because the audit layer is designed to
re-estimate the model from accumulated production telemetry---a path that presumes a
learned estimator rather than a hand-maintained rule set. The contribution is the
late-binding enforcement path, which is unchanged whichever estimator supplies the tier.
```

Also update, elsewhere in the paper:
- The cross-model table gains a **JRip / Weka** row: 0.980 / 0.945 / 0.904 / 99.29% / 93.53%.
- Any wording implying the forest is the best-performing model must be softened to "at the corpus ceiling, alongside other conjunction-capable models."

---

## 9. Reproduction

```powershell
$weka = "C:\Program Files\Weka-3-8-6\weka.jar"
$d    = "F:\ICCIT26\weka"

# Run A -- rule extraction (natural encoding, training set)
java -cp "$weka" weka.classifiers.rules.JRip -O 2 -F 3 -N 2.0 -S 42 `
  -t "$d\access_logs_train.arff" -no-cv > "$d\grid\jrip_rules.txt"

# Run B1 -- natural encoding, held-out test
java -cp "$weka" weka.classifiers.rules.JRip -O 2 -F 3 -N 2.0 -S 42 `
  -t "$d\access_logs_train.arff" -T "$d\access_logs_test.arff" > "$d\grid\jrip_testB1.txt"

# Run B2 -- numeric8, held-out test
java -cp "$weka" weka.classifiers.rules.JRip -O 2 -F 3 -N 2.0 -S 42 `
  -t "$d\access_logs_train_numeric8.arff" -T "$d\access_logs_test_numeric8.arff" `
  > "$d\grid\jrip_testB2.txt"
```

Note: on the command line `-P` *disables* pruning, the inverse of the GUI's `usePruning` checkbox. Omit it to keep pruning on.

---

## 10. Open items

- [ ] **Seed stability** — repeat with seeds 1, 7, 123, 2024; record whether the recovery count and the four thresholds hold.
- [ ] **Verify the error overlap** — intersect JRip's 30 misclassified test rows with the 27 rule-inconsistent rows, to replace the "≈3 genuine errors" inference with a measured figure.
- [ ] **Revise the paper's framing** per §6: add the JRip row to the comparison table, soften any "best model" wording, and restructure the model-choice justification around the bootstrap/probability/retraining arguments.
- [ ] Decide final placement and trim the rule listing to fit six pages.
