## === Run information ===
```
Scheme:       weka.classifiers.meta.AdaBoostM1 -P 100 -S 1 -I 50 -W weka.classifiers.trees.REPTree -- -M 2 -V 0.001 -N 3 -S 1 -L 3 -I 0.0
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
## === Classifier model (full training set) ===
```
AdaBoostM1: Base classifiers and their weights: 

```
## REPTree
```
============

recent_request_count < 8.5
|   failed_attempt_count < 4.5 : 0 (4257/327) [2120/155]
|   failed_attempt_count >= 4.5 : 2 (84/3) [47/0]
recent_request_count >= 8.5
|   recent_request_count < 15.5
|   |   role_customer < 0.5 : 0 (29/5) [14/2]
|   |   role_customer >= 0.5 : 1 (74/6) [33/3]
|   recent_request_count >= 15.5
|   |   role_admin < 0.5 : 2 (210/14) [108/8]
|   |   role_admin >= 0.5 : 1 (12/1) [12/1]

Size of the tree : 11

Weight: 2.51


REPTree
============

record_owner_match < 0.5
|   resource_sensitivity < 0.5
|   |   role_customer < 0.5 : 0 (386.67/90.63) [199.1/56.4]
|   |   role_customer >= 0.5 : 1 (637.66/4.32) [339.82/12.61]
|   resource_sensitivity >= 0.5
|   |   is_office_hours < 0.5 : 1 (337.48/130.81) [212.61/65.41]
|   |   is_office_hours >= 0.5 : 2 (946.49/197.48) [404.14/86.49]
record_owner_match >= 0.5
|   recent_request_count < 8.5
|   |   role_customer < 0.5 : 1 (238.38/145.05) [106.85/73.51]
|   |   role_customer >= 0.5 : 0 (1907.39/262.34) [950.09/119.1]
|   recent_request_count >= 8.5
|   |   role_customer < 0.5 : 1 (49.37/2.16) [27.21/7.21]
|   |   role_customer >= 0.5 : 2 (169.01/76.76) [87.75/35.68]

Size of the tree : 15

Weight: 1.42


REPTree
============

resource_sensitivity < 1.5
|   failed_attempt_count < 4.5
|   |   record_owner_match < 0.5 : 1 (1668.73/880.95) [895.35/437.21]
|   |   record_owner_match >= 0.5 : 0 (1778.41/647.3) [1101.33/498.59]
|   failed_attempt_count >= 4.5 : 2 (148.33/21.22) [71.06/0]
resource_sensitivity >= 1.5
|   role_moderator < 0.5
|   |   record_owner_match < 0.5 : 2 (144.48/60.47) [61.81/11.08]
|   |   record_owner_match >= 0.5 : 0 (170.59/58.87) [98.09/41.68]
|   role_moderator >= 0.5 : 2 (555.38/6.91) [306.44/35.55]

Size of the tree : 11

Weight: 0.47


REPTree
============

resource_sensitivity < 1.5
|   role_customer < 0.5
|   |   recent_request_count < 19 : 0 (1228.7/436.54) [632.96/213.17]
|   |   recent_request_count >= 19 : 1 (136.04/47.24) [48.4/21.93]
|   role_customer >= 0.5
|   |   record_owner_match < 0.5 : 2 (741.21/366.9) [373.42/158.65]
|   |   record_owner_match >= 0.5 : 0 (1704.77/921.36) [942.93/536.35]
resource_sensitivity >= 1.5
|   role_moderator < 0.5 : 0 (248.79/132.96) [220.83/139.96]
|   role_moderator >= 0.5 : 2 (443.73/27.53) [278.2/27.51]

Size of the tree : 11

Weight: 0.27


REPTree
============

resource_sensitivity < 1.5
|   role_customer < 0.5
|   |   recent_request_count < 19.5 : 0 (1172.97/469.43) [646/281.04]
|   |   recent_request_count >= 19.5 : 1 (120.4/52.76) [61.13/27.13]
|   role_customer >= 0.5
|   |   record_owner_match < 0.5 : 1 (710.39/367.44) [416.01/194.08]
|   |   record_owner_match >= 0.5 : 0 (1876.48/1174.98) [856.43/508.78]
resource_sensitivity >= 1.5 : 2 (735.52/289.41) [404.68/72.7]

Size of the tree : 9

Weight: 0.04


REPTree
============

resource_sensitivity < 1.5
|   failed_attempt_count < 4.5
|   |   role_customer < 0.5 : 0 (1250.55/554.39) [680.37/326.7]
|   |   role_customer >= 0.5 : 1 (2359.03/1380.27) [1358.16/780.35]
|   failed_attempt_count >= 4.5 : 2 (142.61/4.65) [76.11/26.04]
resource_sensitivity >= 1.5 : 2 (770.07/268.6) [363.09/100.07]

Size of the tree : 7

Weight: 0.03


REPTree
============

resource_sensitivity < 1.5
|   role_customer < 0.5
|   |   is_office_hours < 0.5 : 1 (413.76/122.64) [143.88/51.04]
|   |   is_office_hours >= 0.5 : 0 (935.13/337.07) [498.96/191.51]
|   role_customer >= 0.5 : 1 (2637.26/1557.33) [1244.2/766.84]
resource_sensitivity >= 1.5 : 2 (780.19/271.01) [346.63/103.97]

Size of the tree : 7

Weight: 0.06


REPTree
============

resource_sensitivity < 1.5
|   role_customer < 0.5
|   |   recent_request_count < 19 : 0 (1185.74/504.22) [602.86/273.06]
|   |   recent_request_count >= 19 : 1 (124.24/63.09) [63.92/21.43]
|   role_customer >= 0.5
|   |   resource_sensitivity < 0.5 : 1 (1555.02/768.55) [847.93/444.06]
|   |   resource_sensitivity >= 0.5 : 2 (1081.23/459.23) [421.98/237.8]
resource_sensitivity >= 1.5
|   role_moderator < 0.5
|   |   record_owner_match < 0.5 : 2 (139.08/60.74) [76.69/35.98]
|   |   record_owner_match >= 0.5 : 0 (150.74/60.17) [130.28/92.28]
|   role_moderator >= 0.5 : 2 (447.18/65.54) [173.13/2.21]

Size of the tree : 13

Weight: 0.24

Number of performed Iterations: 8
```

Time taken to build model: 0.07 seconds

## === Evaluation on test set ===
```
Time taken to test model on supplied test set: 0 seconds
```
## === Summary ===
```
Correctly Classified Instances        1398               93.2    %
Incorrectly Classified Instances       102                6.8    %
Kappa statistic                          0.6929
Mean absolute error                      0.0687
Root mean squared error                  0.1766
Relative absolute error                 38.5413 %
Root relative squared error             59.2407 %
Total Number of Instances             1500     
```
## === Detailed Accuracy By Class ===
```
                 TP Rate  FP Rate  Precision  Recall   F-Measure  MCC      ROC Area  PRC Area  Class
                 0.995    0.416    0.931      0.995    0.962      0.714    0.954     0.984     0
                 0.310    0.001    0.931      0.310    0.466      0.524    0.939     0.813     1
                 0.748    0.004    0.945      0.748    0.835      0.827    0.965     0.890     2
Weighted Avg.    0.932    0.354    0.932      0.932    0.921      0.713    0.954     0.966     
```
## === Confusion Matrix ===
```
    a    b    c   <-- classified as
 1267    2    5 |    a = 0
   59   27    1 |    b = 1
   35    0  104 |    c = 2
```
