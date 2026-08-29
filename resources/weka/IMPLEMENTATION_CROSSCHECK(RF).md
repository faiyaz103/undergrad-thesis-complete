## === Run information ===
```
Scheme:       weka.classifiers.trees.RandomForest -P 100 -I 75 -num-slots 1 -K 0 -M 1.0 -V 0.001 -S 42 -depth 12
Relation:     access_logs_train
Instances:    7000
Attributes:   7
              user_role
              resource_sensitivity
              is_office_hours
              record_owner_match
              recent_request_count
              failed_attempt_count
              risk_level
Test mode:    user supplied test set:  size unknown (reading incrementally)
```
## === Classifier model (full training set) ===
```
RandomForest

Bagging with 75 iterations and base learner

weka.classifiers.trees.RandomTree -K 0 -M 1.0 -V 0.001 -S 42 -depth 12 -do-not-check-capabilities

Time taken to build model: 0.42 seconds
```
## === Evaluation on test set ===
```
Time taken to test model on supplied test set: 0.08 seconds
```
## === Summary ===
```
Correctly Classified Instances        1470               98      %
Incorrectly Classified Instances        30                2      %
Kappa statistic                          0.9229
Mean absolute error                      0.0233
Root mean squared error                  0.1162
Relative absolute error                 13.057  %
Root relative squared error             38.9586 %
Total Number of Instances             1500     
```
## === Detailed Accuracy By Class ===
```
                 TP Rate  FP Rate  Precision  Recall   F-Measure  MCC      ROC Area  PRC Area  Class
                 0.994    0.097    0.983      0.994    0.988      0.920    0.938     0.976     0
                 0.851    0.001    0.974      0.851    0.908      0.905    0.926     0.857     1
                 0.935    0.004    0.956      0.935    0.945      0.940    0.960     0.893     2
Weighted Avg.    0.980    0.083    0.980      0.980    0.980      0.921    0.940     0.962     
```
## === Confusion Matrix ===
```
    a    b    c   <-- classified as
 1266    2    6 |    a = 0
   13   74    0 |    b = 1
    9    0  130 |    c = 2
```