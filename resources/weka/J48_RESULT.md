# J48 (C4.5) — result record and paper guidance

**Status:** Test-partition run complete at default parameters. Validation sweep of `confidenceFactor` not performed (see §7).
**Date:** 2026-08-29
**Purpose:** Add a fourth conjunction-capable model, from a third induction paradigm, to test whether the corpus-saturation pattern holds — and to check whether a single pruned tree can match the deployed ensemble.

---

## 0. Summary of what it says

1. **The saturation pattern holds.** Four models across three induction paradigms now land in 0.973–0.980 weighted F, while every non-conjunctive model sits at 0.821–0.96.
2. **A single pruned tree ties the forest on every aggregate metric** — same 97.80% accuracy, same 0.978 weighted F, same 33 errors.
3. **But it loses on the minority tier.** MEDIUM recall 0.816 against the forest's 0.862; macro F1 0.938 against 0.941. This is the ensemble argument, measured.
4. **It disconfirms a hypothesis.** MEDIUM is *not* pinned at the noise ceiling across all models — see §5.
5. **Seventh independent threshold recovery**, with `failed_attempt_count <= 4` as the root split.

---

## 1. Configuration

| Item | Value |
|---|---|
| Classifier | `weka.classifiers.trees.J48 -C 0.25 -M 2` (defaults) |
| Training data | `access_logs_train_numeric8.arff`, 7,000 rows |
| Test data | `access_logs_test_numeric8.arff`, 1,500 rows, scored once |
| Tree size | 30 leaves, 59 nodes |
| Build time | 0.18 s |

⚠️ **Disclosure:** J48 ran at Weka defaults. SMO and AdaBoost were tuned on the validation partition; J48 was not. This asymmetry must be stated. It is conservative in one direction only — J48 already ties the forest, so tuning could raise it further, not lower it.

---

## 2. Complete result

### 2.1 Pruned tree (full)

```
failed_attempt_count <= 4
|   recent_request_count <= 8
|   |   record_owner_match <= 0
|   |   |   role_customer <= 0
|   |   |   |   resource_sensitivity <= 1
|   |   |   |   |   is_office_hours <= 0
|   |   |   |   |   |   resource_sensitivity <= 0: 0 (164.0/4.0)
|   |   |   |   |   |   resource_sensitivity > 0
|   |   |   |   |   |   |   role_moderator <= 0: 0 (16.0)
|   |   |   |   |   |   |   role_moderator > 0: 1 (52.0/3.0)
|   |   |   |   |   is_office_hours > 0
|   |   |   |   |   |   failed_attempt_count <= 1: 0 (896.0/13.0)
|   |   |   |   |   |   failed_attempt_count > 1
|   |   |   |   |   |   |   role_moderator <= 0
|   |   |   |   |   |   |   |   failed_attempt_count <= 2: 0 (7.0)
|   |   |   |   |   |   |   |   failed_attempt_count > 2: 1 (5.0)
|   |   |   |   |   |   |   role_moderator > 0: 0 (40.0/1.0)
|   |   |   |   resource_sensitivity > 1
|   |   |   |   |   role_moderator <= 0: 0 (22.0/2.0)
|   |   |   |   |   role_moderator > 0: 2 (84.0/4.0)
|   |   |   role_customer > 0
|   |   |   |   resource_sensitivity <= 0: 1 (149.0/5.0)
|   |   |   |   resource_sensitivity > 0: 2 (100.0/4.0)
|   |   record_owner_match > 0
|   |   |   role_moderator <= 0: 0 (4651.0/52.0)
|   |   |   role_moderator > 0
|   |   |   |   resource_sensitivity <= 1
|   |   |   |   |   is_office_hours <= 0
|   |   |   |   |   |   resource_sensitivity <= 0: 0 (26.0)
|   |   |   |   |   |   resource_sensitivity > 0: 1 (14.0)
|   |   |   |   |   is_office_hours > 0: 0 (133.0/2.0)
|   |   |   |   resource_sensitivity > 1: 2 (18.0/2.0)
|   recent_request_count > 8
|   |   recent_request_count <= 15
|   |   |   role_customer <= 0
|   |   |   |   resource_sensitivity <= 1
|   |   |   |   |   is_office_hours <= 0
|   |   |   |   |   |   failed_attempt_count <= 1: 0 (7.0/1.0)
|   |   |   |   |   |   failed_attempt_count > 1: 1 (2.0)
|   |   |   |   |   is_office_hours > 0: 0 (29.0)
|   |   |   |   resource_sensitivity > 1: 2 (4.0/1.0)
|   |   |   role_customer > 0
|   |   |   |   record_owner_match <= 0
|   |   |   |   |   resource_sensitivity <= 0: 0 (2.0/1.0)
|   |   |   |   |   resource_sensitivity > 0: 2 (4.0)
|   |   |   |   record_owner_match > 0: 1 (98.0/1.0)
|   |   recent_request_count > 15
|   |   |   role_admin <= 0
|   |   |   |   role_customer <= 0
|   |   |   |   |   record_owner_match <= 0
|   |   |   |   |   |   recent_request_count <= 27
|   |   |   |   |   |   |   resource_sensitivity <= 1: 1 (4.0/1.0)
|   |   |   |   |   |   |   resource_sensitivity > 1: 2 (2.0)
|   |   |   |   |   |   recent_request_count > 27: 2 (46.0)
|   |   |   |   |   record_owner_match > 0: 1 (11.0/1.0)
|   |   |   |   role_customer > 0: 2 (244.0/7.0)
|   |   |   role_admin > 0: 1 (23.0/1.0)
failed_attempt_count > 4: 2 (147.0/4.0)

Number of Leaves  : 30
Size of the tree  : 59
```

### 2.2 Test-partition metrics

Accuracy **97.80%** (1467/1500), Kappa 0.9148, weighted F **0.978**, macro F **0.938**.

| Class | TP Rate | FP Rate | Precision | Recall | F | MCC | ROC | PRC |
|---|---|---|---|---|---|---|---|---|
| LOW (0) | 0.994 | 0.106 | 0.981 | 0.994 | 0.988 | 0.915 | 0.959 | 0.986 |
| MEDIUM (1) | 0.816 | 0.002 | 0.959 | 0.816 | 0.882 | 0.879 | 0.942 | 0.876 |
| HIGH (2) | 0.935 | 0.004 | 0.956 | 0.935 | 0.945 | 0.940 | 0.968 | 0.898 |
| Weighted avg | 0.978 | 0.091 | 0.978 | 0.978 | 0.978 | 0.915 | 0.958 | 0.972 |

Confusion matrix:

```
    a    b    c   <-- classified as
 1266    2    6 |  a = LOW
   16   71    0 |  b = MEDIUM
    8    1  130 |  c = HIGH
```

Derived: LOW pass rate 1266/1274 = **99.37%**; HIGH interception 130/139 = **93.53%**; MEDIUM recall 71/87 = **0.816**.

---

## 3. Against the other models (same test partition)

| Model | Acc | Weighted F | **Macro F** | MED F1 | MED recall | LOW pass | HIGH intercept | Errors |
|---|---|---|---|---|---|---|---|---|
| JRip | 0.980 | 0.980 | **0.945** | 0.904 | 0.862 | 99.29% | 93.53% | 30 |
| Random forest | 0.978 | 0.978 | **0.941** | 0.893 | 0.862 | 99.14% | 92.81% | 33 |
| **J48** | 0.978 | 0.978 | **0.938** | 0.882 | **0.816** | 99.37% | 93.53% | 33 |
| sklearn tree ($d{=}12$) | 0.973 | 0.973 | 0.925 | not computed | not computed | 98.59% | 92.09% | 41 |

**Error composition differs despite the identical count.** The forest errs 11/12/10 across the LOW/MEDIUM/HIGH rows; J48 errs 8/16/9. J48 is better on LOW and HIGH, worse on MEDIUM.

---

## 4. What the result says

### 4.1 The saturation pattern is now solid

| Conjunction-capable | Weighted F | Not conjunction-capable | Weighted F |
|---|---|---|---|
| JRip (RIPPER) | 0.980 | RBF SVM (tuned) | ≈0.96 |
| Random forest (bagged CART) | 0.978 | AdaBoost + stumps | 0.856 |
| **J48 (C4.5)** | **0.978** | Logistic regression (balanced) | 0.821 |
| sklearn tree (CART) | 0.973 | Majority class | 0.780 |

Four models spanning three induction paradigms — gain-ratio with error-based pruning (C4.5), Gini with depth limiting (CART), and sequential covering (RIPPER) — all land within 0.007 of one another. Every model that cannot represent axis-aligned conjunctions fails, and fails specifically on the MEDIUM tier.

### 4.2 The ensemble argument, measured

This is the most useful thing J48 contributes. It is **indistinguishable from the forest on every aggregate metric** — same accuracy to four decimals, same weighted F, same error count — yet:

- MEDIUM recall **0.816 vs 0.862** (71 of 87 against 75 of 87)
- MEDIUM F1 **0.882 vs 0.893**
- Macro F1 **0.938 vs 0.941**

The paper has been asserting that aggregate metrics hide the minority-class gap. This is the cleanest demonstration of it in the entire result set: two models that look identical on the headline number differ measurably on the tier the graduated policy depends on.

**Be precise about scope.** This justifies an ensemble over a *single tree*. It does nothing about JRip, which still exceeds the forest on every metric including macro F1 (0.945 vs 0.941). The reframing in §6 of `JRIP_RULE_RECOVERY.md` stands unchanged.

### 4.3 Threshold recovery — the seventh

The root split is `failed_attempt_count <= 4`, with the `> 4` branch resolving directly to HIGH at 147/4. That is generator rule 6 (`f ≥ 5 → HIGH`, unconditional) recovered as a single root branch — appropriate, since it is the only rule with no role or resource antecedent.

Beneath it, `recent_request_count <= 8` and `<= 15` are the MEDIUM entry (`v ≥ 9`) and HIGH velocity (`v > 15`) boundaries, both exact. Further conjunctions recovered:

| Tree path | Generator rule |
|---|---|
| `customer ∧ owner<=0 ∧ sensitivity<=0 : 1` | 7 — customer ∧ ¬owner ∧ LOW → MED |
| `customer ∧ owner<=0 ∧ sensitivity>0 : 2` | 1 — customer ∧ ¬owner ∧ {MED,HIGH} → HIGH |
| `8 < v ≤ 15 ∧ customer ∧ owner>0 : 1 (98.0/1.0)` | 8 — customer ∧ 9 ≤ v ≤ 15 → MED |
| `moderator ∧ sensitivity>1 : 2` | 3 — moderator ∧ HIGH → HIGH |
| `moderator ∧ sensitivity>0 ∧ ¬office : 1` | 9 — moderator ∧ ¬hours ∧ MED → MED |
| `v > 15 ∧ admin : 1 (23.0/1.0)` | 11 — (mod ∨ admin) ∧ v > 18 → MED (approximate) |

The `recent_request_count > 27` split approximates rule 4 (`moderator ∧ v > 25`) but is not exact.

---

## 5. A hypothesis this result disconfirms

It was previously proposed that MEDIUM might be pinned at the label-noise ceiling for all conjunction-capable models. Of the 87 MEDIUM test rows, 11 carry redrawn labels contradicting the generator, so the achievable ceiling is 76/87 = 0.874.

- Random forest: 75/87 — one short of achievable
- JRip: 75/87 — one short of achievable
- **J48: 71/87 — five short**

**The hypothesis is false and should not be written up.** MEDIUM retains real discriminating power; the forest's and JRip's MEDIUM performance is an achievement, not an artefact of every model hitting the same wall. This is favourable to the paper — it means the ensemble is doing something a single pruned tree cannot.

---

## 6. How to portray it in the paper — concretely

### 6.1 One table row

Add to the cross-model comparison table, 3 dp for consistency:

```latex
J48 (C4.5, pruned)  & Weka & 0.978 & 0.938 & 0.882 & 99.37\% & 93.53\% \\
```

### 6.2 One passage in Section V-B

Place immediately after the model-comparison table, before the feature-importance discussion:

```latex
Two results in Table~\ref{tab:models} are worth separating from the ranking. First, every
model able to represent axis-aligned conjunctions---a rule list, a pruned C4.5 tree, a
depth-limited CART tree, and the bagged ensemble---reaches 0.973--0.980 weighted F1,
while logistic regression, an RBF kernel and boosted stumps do not exceed 0.96 and fail
specifically on the \MED{} tier. The corpus is therefore saturated by a representational
property rather than by any particular learner.

Second, the pruned C4.5 tree is indistinguishable from the forest on every aggregate
metric---0.978 weighted F1, 97.80\% accuracy, 33 test errors for both---yet reaches only
0.816 \MED{} recall against the forest's 0.862, and 0.938 macro F1 against 0.941. The
two models differ measurably precisely on the tier the graduated policy depends on, and
not at all on the headline figure. This is the concrete form of the argument that
aggregate accuracy is the wrong metric for this problem.
```

### 6.3 One clause in the threshold-recovery sentence

Wherever the paper lists the independent recoveries of the generator's cutoffs, add J48:

```latex
... the C4.5 root split at $f \le 4$ ...
```

### 6.4 What NOT to include

- **Do not print the tree.** 30 leaves and 59 nodes will not fit six pages. JRip's 14 rules are the better artifact for the same point, and printing both is redundant.
- **Do not present the tied accuracy as a finding.** 1467/1500 twice is a coincidence at this sample size. The signal is the macro-F1 and MEDIUM gap; lead with those.
- **Do not claim J48 confirms a MEDIUM ceiling.** See §5.

### 6.5 Space cost

One table row plus roughly one-sixth of a column of text. The threshold clause is free — it joins a sentence that already exists.

---

## 7. Solidity and open items

**Firm:** single evaluation on the quarantined partition, same encoding and partitions as every other model, deterministic (J48 has no random component at these settings), and the tree is directly inspectable against `dataset/script.py`.

**Weaknesses:**

1. **Untuned.** Defaults `-C 0.25 -M 2`, whereas SMO and AdaBoost were tuned on validation. Disclose it. *Fix: sweep `confidenceFactor` ∈ {0.1, 0.25, 0.5} and `minNumObj` ∈ {2, 5} on the validation partition.* Note the likely direction — tuning would raise J48, which weakens rather than strengthens the case for the forest.
2. **Margins are small.** The forest's macro-F1 advantage is 0.003, roughly four MEDIUM rows. Describe it as a consistent direction, not a decisive gap, and note that it is corroborated by MEDIUM recall (0.862 vs 0.816), which is the larger and more interpretable difference.
3. **Run on `numeric8` only.** No natural-encoding variant was produced, so the tree reads as `role_customer > 0` rather than `user_role = customer`. Since the tree is not being printed, this does not matter — but it should not be described as a readable artifact in the paper.

**Open items:**

- [ ] Validation sweep of `confidenceFactor` / `minNumObj`, for parity with the tuned baselines.
- [ ] Per-class figures for the scikit-learn decision-tree row, currently missing from the comparison table.

---

## 8. Reproduction

```powershell
$weka = "C:\Program Files\Weka-3-8-6\weka.jar"
$d    = "F:\ICCIT26\weka"

java -cp "$weka" weka.classifiers.trees.J48 -C 0.25 -M 2 `
  -t "$d\access_logs_train_numeric8.arff" -T "$d\access_logs_test_numeric8.arff" `
  > "$d\grid\j48_test.txt"
```
