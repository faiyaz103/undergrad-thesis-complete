# Part D — RBF-kernel SVM: process record

**Status:** D1–D2 complete. D3 (final test-set run) and the class-balancing check are outstanding.
**Date of runs:** 2026-08-29
**Purpose:** Produce a tuned RBF-SVM row for the multi-model comparison table, as an independent-implementation baseline against the deployed random forest.

---

## 1. Configuration

| Item | Value |
|---|---|
| Tool | Weka `weka.classifiers.functions.SMO` (core; no package install) |
| Kernel | `weka.classifiers.functions.supportVector.RBFKernel` |
| Multi-class strategy | Pairwise one-vs-one (matches scikit-learn `SVC`) |
| Training file | `access_logs_train_numeric8.arff` (7,000 rows) |
| Tuning file | `access_logs_val_numeric8.arff` (1,500 rows) |
| Test file | `access_logs_test_numeric8.arff` (1,500 rows) — **not yet used** |
| `filterType` | Normalize training data (SMO default; stands in for `StandardScaler`) |
| Output model | Disabled via **More options...**, to keep transcripts readable |
| Selection metric | Validation weighted F-measure |

### Why the `numeric8` encoding

The `numeric8` ARFF files reproduce the exact 8-element vector the deployed pipeline uses: one-hot role, ordinal sensitivity (LOW=0, MEDIUM=1, HIGH=2), pass-through counts. Under the natural nominal encoding, Weka would expand `resource_sensitivity` into three binary indicators and discard its ordering, which materially changes behaviour for a kernel method. Using `numeric8` keeps the comparison anchored to the feature vector actually shipped.

### Protocol

All hyperparameter search was carried out against the **validation** partition. The test partition has not been touched during Part D and is reserved for a single final run in D3.

---

## 2. Run log

### 2.1 Initial grid (D2 as specified)

3 × 3 grid, `c` ∈ {1, 10, 100} × `gamma` ∈ {0.01, 0.1, 0.5}. Validation weighted F-measure:

| c \ gamma | 0.01 | 0.1 | 0.5 |
|---|---|---|---|
| **1** | 0.874 | 0.921 | 0.955 |
| **10** | 0.908 | 0.957 | 0.961 |
| **100** | 0.928 | 0.960 | **0.962** |

**Observation:** the score increased monotonically along both axes, with the maximum at the top-right corner of the searched range. Per the stated stopping rule, a corner optimum means the true optimum may lie outside the box, so the search could not be declared complete.

### 2.2 Corner extension (deviation from the original plan)

The guide specified a single 3 × 3 grid. Because the optimum sat at the corner, the search was extended by one step on each axis: `c` ∈ {100, 1000} × `gamma` ∈ {0.5, 1.0, 2.0}. The cell `(100, 0.5)` was already known and was re-run to capture per-class recalls.

Run through the Weka Explorer GUI. Per-class recall added in this pass.

| c | gamma | Val weighted F | MEDIUM recall (class 1) | HIGH recall (class 2) |
|---|---|---|---|---|
| 100 | 0.5 | 0.962 | 0.568 | 0.928 |
| 100 | 1.0 | 0.962 | 0.580 | 0.921 |
| 100 | 2.0 | 0.965 | 0.614 | 0.935 |
| 1000 | 0.5 | 0.964 | 0.614 | 0.914 |
| 1000 | 1.0 | **0.966** | 0.625 | 0.935 |
| 1000 | 2.0 | 0.965 | 0.625 | 0.935 |

**Total cells evaluated: 14** — a staged search (3 × 3, then a targeted 2 × 3 corner extension), not a full 4 × 5 cross product. This should be described accurately in the paper; the two axes were not exhaustively crossed.

Transcripts follow the naming convention `F:\ICCIT26\weka\grid\smo_C<c>_G<gamma>.txt`.

---

## 3. Findings

### 3.1 The search is complete

Two independent reasons:

1. **An interior maximum was found.** Along `c = 1000`, the score runs 0.964 → **0.966** → 0.965 as gamma goes 0.5 → 1.0 → 2.0. The optimum is bracketed rather than running off the edge of the grid.
2. **The plateau is flat.** Every cell from `(10, 0.5)` through `(1000, 1.0)` falls in 0.961–0.966. A 100× increase in `c` bought 0.004 weighted F — noise on a 1,500-row partition.

No further extension is warranted.

### 3.2 The deficit is concentrated in the MEDIUM tier

| Model | MEDIUM recall | HIGH recall |
|---|---|---|
| RBF SVM (best cells) | 0.57 – 0.63 | 0.91 – 0.94 |
| Random forest | 0.8621 | 0.9281 |

⚠️ **Partition caveat:** SVM figures are validation; random-forest figures are from the scikit-learn test-set evaluation. Different partitions of the same distribution, so the gap is indicative only until D3 places both on the test partition.

The SVM is **competitive on HIGH risk** — 0.935 at its best, marginally above the forest. Its weakness is almost entirely in **MEDIUM**, missing roughly 40% of cases against the forest's 14%.

### 3.3 Why this matters for the framework

MEDIUM is the tier the graduated policy depends on. A model that handles LOW and HIGH but cannot locate the middle band collapses the three-tier policy back into binary allow/deny — the exact limitation the framework is designed to overcome.

The mechanism is visible in the generator's own label rules: MEDIUM is defined by *interval* conditions such as `customer ∧ 9 ≤ v ≤ 15` — a narrow, axis-aligned box covering 5.8% of the data. A decision tree isolates it with two comparisons; an RBF kernel with a single global bandwidth smooths across it. This is a mechanistic argument for tree ensembles on this problem, stronger than the assertion currently in Section III-D of the paper.

A secondary signal points the same way: the score improves as `gamma` grows, meaning the model wants an ever tighter, more local boundary. That is what one would predict when the true labels are sharp axis-aligned thresholds (`v > 15`, `f ≥ 5`) — the kernel is pushed toward near-memorisation to imitate what a tree expresses in a single split.

---

## 4. Selected configuration

**`c` = 100, `gamma` = 2.0** (validation weighted F 0.965).

Rationale: within 0.001 of the observed maximum, trains an order of magnitude faster than `c = 1000`, and its per-class recalls (0.614 / 0.935) match the best cells on the plateau. Justifiable in one clause — within noise of the optimum at a tenth of the cost.

---

## 5. Outstanding work

### 5.1 Class-balancing fairness check (do before D3)

The deployed random forest was trained with `class_weight='balanced'`; SMO has no equivalent option, so as it stands the comparison is tilted toward the forest — and MEDIUM recall is precisely where that bias would surface. This is a foreseeable reviewer objection.

Procedure, against the **validation** file:

1. **Choose** → `meta` → **FilteredClassifier**
2. Open its config; set `classifier` → **SMO** with `c` = 100, `kernel` = **RBFKernel**, `gamma` = 2.0
3. Set `filter` → `supervised` → `instance` → **ClassBalancer**
4. **Start**

Compare MEDIUM recall against 0.614:

- **Substantially higher** → adopt the balanced variant as the SVM row; that is the like-for-like comparison.
- **Roughly unchanged** → the deficit is structural, not a class-weighting artefact. This is the stronger claim, and should be stated.

### 5.2 D3 — final test run

Run the selected configuration (balanced or unbalanced, per 5.1) **once** against `access_logs_test_numeric8.arff`. Record accuracy, weighted F, per-class precision/recall/F for all three classes, and the confusion matrix.

---

## 6. Reproduction

### GUI

1. **Preprocess** → **Open file...** → `access_logs_train_numeric8.arff`
2. **Classify** → **Supplied test set** → **Set...** → `access_logs_val_numeric8.arff` → **Close**
3. **More options...** → untick **Output model** → **OK**
4. **Choose** → `functions` → **SMO**
5. Click the config *text line* (not the button) → set `c` → click `kernel` → **Choose** → **RBFKernel** → set `gamma` → **OK** → **OK**
6. Verify the config line shows the intended `-C` (SMO complexity) and `-G` (kernel gamma); the trailing `-C 250007` is the kernel cache and is unrelated
7. **Start**; then right-click the Result list entry → **Save result buffer**

### Command line

```powershell
$weka = "C:\Program Files\Weka-3-8-6\weka.jar"
$d    = "F:\ICCIT26\weka"
$tr   = "$d\access_logs_train_numeric8.arff"
$val  = "$d\access_logs_val_numeric8.arff"

$a = @('-C','100','-N','0','-o','-v',
       '-K','weka.classifiers.functions.supportVector.RBFKernel -G 2.0',
       '-t',$tr,'-T',$val)
java -cp "$weka" weka.classifiers.functions.SMO @a
```

`-o` suppresses the model dump, `-v` suppresses training-set statistics. Uppercase `-C` is SMO's complexity constant; lowercase `-c` would be Weka's class-index option — they are different flags.

---

## 7. For the paper

Report, at minimum:

- The search performed: 3 × 3 grid over `c` ∈ {1, 10, 100} × `gamma` ∈ {0.01, 0.1, 0.5}, extended to `c` ∈ {100, 1000} × `gamma` ∈ {0.5, 1.0, 2.0} after the optimum appeared at the corner. 14 configurations total.
- The selection criterion (validation weighted F-measure) and the chosen values.
- Whether class balancing was applied.
- Test-set accuracy, weighted F, macro F, and per-class recall — with MEDIUM recall called out explicitly.

This is what makes the row defensible as a tuned baseline rather than a strawman. The MEDIUM-tier deficit is the substantive result and deserves a sentence in the results discussion, not just a table cell.

**Encoding and weighting differences to disclose:** Weka's SMO normalises internally rather than standardising; there is no class-weight parameter; and the multi-class decomposition is pairwise. These make the row a fair tuned baseline, not a like-for-like replication of a scikit-learn `SVC` run.
