## === Run information ===
```
Scheme:       weka.classifiers.functions.SMO -C 100.0 -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 -K "weka.classifiers.functions.supportVector.RBFKernel -C 250007 -G 2.0" -calibrator "weka.classifiers.functions.Logistic -R 1.0E-8 -M -1 -num-decimal-places 4"
Relation:     access_logs_train_numeric8
Instances:    7000
Attributes:   9
              role_customer
              role_moderator
              role_admin
              resource_sensitivity
              is_office_hours
              record_owner_match
              recent_request_count
              failed_attempt_count
              risk_level
Test mode:    user supplied test set:  size unknown (reading incrementally)
```
## === Evaluation on test set ===
```
Time taken to test model on supplied test set: 0.07 seconds
```
## === Summary ===
```
Correctly Classified Instances        1448               96.5333 %
Incorrectly Classified Instances        52                3.4667 %
Kappa statistic                          0.8613
Mean absolute error                      0.2319
Root mean squared error                  0.2893
Relative absolute error                130.1451 %
Root relative squared error             97.0366 %
Total Number of Instances             1500     
```
## === Detailed Accuracy By Class ===
```
                 TP Rate  FP Rate  Precision  Recall   F-Measure  MCC      ROC Area  PRC Area  Class
                 0.993    0.181    0.969      0.993    0.981      0.865    0.905     0.968     0
                 0.621    0.003    0.931      0.621    0.745      0.749    0.822     0.601     1
                 0.928    0.005    0.949      0.928    0.938      0.932    0.967     0.896     2
Weighted Avg.    0.965    0.155    0.965      0.965    0.963      0.865    0.906     0.940     
```
## === Confusion Matrix ===
```
    a    b    c   <-- classified as
 1265    2    7 |    a = 0
   33   54    0 |    b = 1
    8    2  129 |    c = 2
```
