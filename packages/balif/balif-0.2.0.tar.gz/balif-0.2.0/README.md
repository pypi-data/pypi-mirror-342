# BALIF: Bayesian Active Learning Isolation Forest

**Version:** 0.1.2  
**License:** MIT  

## Description
Convert unsupervised tree ensembles into Bayesian Anomaly Detectors (**BAD**) that can be updated dynamically. **BAD** models are build on top of the popular [PyOD](https://github.com/yzhao062/pyod) and keep the original interface, while adding cool new capabilities for:
- **Weakly Supervised Learning**
- **Active Learning**
- **Lifelong Learning**



## Installation

Install BALIF using pip:

```bash
pip install balif
```

## Usage

### PyOD Compatibility

BAD model maintain the same interface as PyOD, making it easy to integrate into existing workflows. The core methods like `fit()`, `decision_function()`, and `predict()` work exactly the same way as in standard PyOD models. This allows users to seamlessly switch between regular PyOD models and BALIF's Bayesian versions with minimal code changes.

```python
from pyod.models.iforest import IForest
from balif import BADIForest
import numpy as np

# Generate some data
X_inliers = np.random.randn(1000, 5)
X_outliers = np.random.uniform(low=-4, high=4, size=(50, 5))
X_train = np.concatenate([X_inliers, X_outliers], axis=0)

# BAD model follow the PyOD interface
pyod_model = IForest().fit(X_train)
bad_model = BADIForest().fit(X_train)

# Get anomaly scores
scores = pyod_model.decision_function(X_train)
scores = bad_model.decision_function(X_train)

# Predict if points are anomalies
predictions = pyod_model.predict(X_train)
predictions = bad_model.predict(X_train)
```

### Incremental Learning with .update()

BAD models support incremental learning through the `.update()` method, allowing you to update the model with new data without retraining from scratch:

```python
# New labelled data becomes available
X_new = np.random.randn(100, 5)
y_new = np.array([0] * 90 + [1] * 10)  # 0: normal, >=1: anomaly

# Update the model with the new data
bad_model.update(X_new, y_new)

# The model now incorporates knowledge from both datasets
updated_scores = bad_model.decision_function(X_test)
```

> **Note:** For some applications, it might be necessary to recompute the contamination threshold after updating the model, especially if the distribution of your data changes significantly over time.

### Active Learning with the AL Module

BALIF includes an active learning module that helps identify the most informative instances for labeling:

```python
from balif import active_learning, BADIForest

# Generate data and fit model
X_inliers = np.random.randn(1000, 5)
X_outliers = np.random.uniform(low=-4, high=4, size=(50, 5))
X_train = np.concatenate([X_inliers, X_outliers], axis=0)
model = BADIForest().fit(X_train)

# get top-k most interesting points 
queries_idx = active_learning.get_queries_independent(
    model, X_train, interest_method="margin", batch_size=10
)
```

The active learning module offers several query strategies:
- `'margin'`: Prioritize instances with predictions close to the decision boundary.
- `'anom'`: Prioritize instances with high anomaly score
- `'bald'`: Prioritize instances with high mutual entropy between prediction and parameters 

Active learning can significantly reduce the labeling effort while maintaining high model performance.


### Batteries included with ODDS dataset

BALIF provides easy access to benchmark anomaly detection datasets from the [Outlier Detection DataSets (ODDS)](http://odds.cs.stonybrook.edu/) repository:
```python
from balif import odds_datasets

# Show included Datasets from ODDS
for name in odds_datasets.dataset_names:
    X, y = odds_datasets.load(name)
    print(f"DATASET: {dataset}")
    print(f"X: {X.shape}")
    print(f"contamination: {100*y.mean():.2f}%")
    print()
```