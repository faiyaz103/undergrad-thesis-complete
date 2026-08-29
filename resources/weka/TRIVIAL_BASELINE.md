# ZeroR
## === Run information ===
```
Scheme:       weka.classifiers.rules.ZeroR 
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
ZeroR predicts class value: 0

Time taken to build model: 0 seconds
```
## === Evaluation on test set ===
```
Time taken to test model on supplied test set: 0.01 seconds
```
## === Summary ===
```
Correctly Classified Instances        1274               84.9333 %
Incorrectly Classified Instances       226               15.0667 %
Kappa statistic                          0     
Mean absolute error                      0.1781
Root mean squared error                  0.2982
Relative absolute error                100      %
Root relative squared error            100      %
Total Number of Instances             1500     
```
## === Detailed Accuracy By Class ===
```
                 TP Rate  FP Rate  Precision  Recall   F-Measure  MCC      ROC Area  PRC Area  Class
                 1.000    1.000    0.849      1.000    0.919      ?        0.500     0.849     0
                 0.000    0.000    ?          0.000    ?          ?        0.500     0.058     1
                 0.000    0.000    ?          0.000    ?          ?        0.500     0.093     2
Weighted Avg.    0.849    0.849    ?          0.849    ?          ?        0.500     0.733     
```
## === Confusion Matrix ===
```
    a    b    c   <-- classified as
 1274    0    0 |    a = 0
   87    0    0 |    b = 1
  139    0    0 |    c = 2
```

---
# OneR

## === Run information ===
```
Scheme:       weka.classifiers.rules.OneR -B 6
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
recent_request_count:
	< 8.5	-> 0
	< 13.5	-> 1
	< 15.5	-> 0
	>= 15.5	-> 2
(6296/7000 instances correct)

Time taken to build model: 0.01 seconds
```
## === Evaluation on test set ===
```
Time taken to test model on supplied test set: 0.01 seconds
```
## === Summary ===
```
Correctly Classified Instances        1353               90.2    %
Incorrectly Classified Instances       147                9.8    %
Kappa statistic                          0.5158
Mean absolute error                      0.0653
Root mean squared error                  0.2556
Relative absolute error                 36.6735 %
Root relative squared error             85.7296 %
Total Number of Instances             1500     
```
## === Detailed Accuracy By Class ===
```
                 TP Rate  FP Rate  Precision  Recall   F-Measure  MCC      ROC Area  PRC Area  Class
                 0.992    0.597    0.904      0.992    0.946      0.564    0.697     0.903     0
                 0.310    0.004    0.818      0.310    0.450      0.488    0.653     0.294     1
                 0.446    0.004    0.912      0.446    0.599      0.616    0.721     0.458     2
Weighted Avg.    0.902    0.508    0.899      0.902    0.885      0.564    0.697     0.827     
```
## === Confusion Matrix ===
```
    a    b    c   <-- classified as
 1264    6    4 |    a = 0
   58   27    2 |    b = 1
   77    0   62 |    c = 2
```
