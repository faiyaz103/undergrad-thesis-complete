## Background:
Secure backend systems uses Transparent Data Encryption for data at rest, Application Level Encryption(field level) for data before storage. When an authenticated and authorized user access data, db engine decrypts the data, give to application, application performs decryption, and the response reaches to the user. 

## Problem:
In case of credential breach, IDOR attack, stolen credentials, user miss-use, there is no mechanism to check the behavior of the user, the decryption happens automatically for any authenticated and authorized user. So there is a chance of sensitive data getting in wrong hands.

## Proposed Methodology:
Proposing a backend framework where the system fetches or extracts features from a user request, from their it predicts risk score, labels are high, medium, low. For high risk access gets denied, for medium risk partial decryption happens, for low risk complete decryption happens.

## Dataset generation:
synthetic rule based, since this is a framework, dataset generation for model training maybe different for different systems.

## Model selection:
Logistic regression baseline, used random forest classifier to predict risks, since this is a framework models maybe different for a different system.

## Model integration:
transpilation technique

## Result analysis:
used weka, give me step by step guide to use weka for generating result

## theme of the work:
Proposing a framework for ml-based adaptive data access for data in runtime or if it is not appropriate suggest something accurate and appropriate
