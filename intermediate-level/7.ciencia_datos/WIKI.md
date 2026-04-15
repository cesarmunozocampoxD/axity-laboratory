# Data and Machine Learning in Python

## 1. Purpose

This wiki gives a medium-length overview of three connected topics in the Python data and machine learning ecosystem:

- **NumPy, Polars, and pandas**
- **scikit-learn classical models**
- **model serialization and basic inference**

These topics belong together because a practical machine learning workflow often looks like this:

1. load and transform data
2. represent it efficiently
3. train a model
4. persist the model
5. run inference later on new data

The goal of this guide is not to cover every API detail.  
The goal is to build a strong mental model for how these tools fit together and when to use each one.

---

## 2. A practical ecosystem view

A useful high-level view is:

- **NumPy** is the foundation for array-based numerical computing
- **pandas** is a flexible and widely used labeled table library
- **Polars** is a modern, performance-oriented DataFrame library with strong lazy execution support
- **scikit-learn** is the standard classical machine learning toolkit for Python
- **model persistence** connects training to deployment and later inference

If you understand those roles clearly, most decisions in this area become much easier.

---

# Part I — NumPy, Polars, and pandas

## 3. NumPy

### What NumPy is
NumPy is the core numerical computing library in Python.

Its central concept is the **`ndarray`**, which NumPy defines as a multidimensional, homogeneous array of fixed-size items. citeturn126053search0turn126053search4

### Why it matters
NumPy matters because it gives Python:
- fast array-oriented operations
- vectorized computation
- broadcasting
- numerical building blocks used by many scientific libraries

### What it is best for
NumPy is strongest when your data is:
- numeric
- homogeneous
- naturally array-shaped
- computation-heavy

Typical uses include:
- matrix operations
- scientific calculations
- feature arrays
- numerical preprocessing
- simulations

### Pythonic mental model
Think of NumPy as:

> “The array and numeric computation layer.”

It is not mainly a table-analysis tool.  
It is the lower-level numerical substrate.

---

## 4. pandas

### What pandas is
pandas centers on the **DataFrame**, which the official docs describe as two-dimensional, size-mutable, potentially heterogeneous tabular data with labeled axes. citeturn126053search1

### Why it matters
pandas is the dominant Python tool for:
- tabular analysis
- spreadsheet-like manipulation
- CSV and SQL-style workflows
- exploratory data analysis
- handling missing data
- time series work

### What it is best for
pandas is usually the natural choice when:
- columns have names and meaning
- data types differ by column
- joins, groupbys, and reshaping matter
- labels are central to the analysis

### Pythonic mental model
Think of pandas as:

> “The labeled tabular analysis layer.”

Where NumPy thinks in arrays, pandas thinks in labeled tables.

---

## 5. Polars

### What Polars is
Polars is a modern DataFrame library. Its documentation distinguishes both **DataFrame** and **LazyFrame**, and describes `LazyFrame` as a lazy computation graph that supports whole-query optimization and parallelism. citeturn126053search2turn126053search14

### Why it matters
Polars is important because it offers:
- high-performance DataFrame processing
- expression-based workflows
- lazy execution
- query optimization
- strong fit for modern data pipelines

### What it is best for
Polars is especially attractive when:
- performance matters a lot
- transformations are pipeline-heavy
- lazy query planning is useful
- the workload is tabular but larger or more performance-sensitive

### Pythonic mental model
Think of Polars as:

> “The performance-oriented modern DataFrame layer.”

It overlaps with pandas, but its style often feels more query-oriented and optimization-aware.

---

## 6. Comparing NumPy, pandas, and Polars

A simple practical comparison is:

### NumPy
Use when:
- the problem is numerical and array-based
- homogeneous typed arrays are the right abstraction
- you care about vectorized math more than labeled tables

### pandas
Use when:
- the problem is tabular and label-oriented
- flexibility matters
- ecosystem compatibility matters
- exploratory analysis is central

### Polars
Use when:
- the problem is tabular
- performance matters strongly
- a pipeline/expression style fits the workload
- lazy execution offers a real advantage

### Important practical point
These libraries are not enemies.  
They often complement each other.

A realistic project may:
- use Polars or pandas for transformation
- convert to NumPy for modeling
- use pandas for final inspection or reporting

---

## 7. Eager vs lazy thinking

One of the biggest conceptual differences here is between:
- **eager execution**
- **lazy execution**

pandas is usually experienced as a more eager, step-by-step table workflow.  
Polars can work eagerly too, but its lazy mode is one of its main strengths, and `.lazy()` creates a `LazyFrame` whose operations are only executed when you later materialize the result. citeturn126053search6turn126053search18

This matters because it changes how you think about data processing:
- pandas often feels procedural
- Polars can feel more like building an optimized query plan

---

# Part II — scikit-learn Classical Models

## 8. What “classical models” means

In this context, “classical models” means the major non-deep-learning machine learning families provided through scikit-learn’s estimator API.

The official scikit-learn user guide organizes the library around supervised and unsupervised learning families such as linear models, support vector machines, neighbors, trees, ensembles, clustering, and Gaussian mixture models. citeturn126053search7turn126053search11

These models remain extremely important because they are often:
- strong baselines
- efficient to train
- effective on structured/tabular data
- easier to explain than deep learning systems

---

## 9. The common estimator model

One reason scikit-learn is so widely used is its very consistent estimator API.

A common mental model is:

```python
model.fit(X_train, y_train)
preds = model.predict(X_test)
```

This consistency makes it easier to compare models and swap them during experimentation.

---

## 10. Main supervised model families

### Linear models
Examples:
- Linear Regression
- Ridge
- Lasso
- Elastic Net
- Logistic Regression

Use them when:
- interpretability matters
- baseline performance matters
- relationships are approximately linear or can be made so through features

### Support Vector Machines
Examples:
- `SVC`
- `SVR`
- `LinearSVC`
- `LinearSVR`

Use them when:
- classical strong classifiers are needed
- the dataset is not huge
- boundaries may be more complex than simple linear models

### k-Nearest Neighbors
Examples:
- `KNeighborsClassifier`
- `KNeighborsRegressor`

Use them when:
- local similarity is meaningful
- you want a simple baseline
- prediction cost is acceptable

### Trees and ensembles
Examples:
- Decision Trees
- Random Forests
- Gradient Boosting / HistGradientBoosting

Use them when:
- tabular data is central
- nonlinearities matter
- interactions between features matter
- strong practical baseline performance is needed

### Naive Bayes
Use it when:
- you need fast probabilistic baselines
- text-like or count-based classification is involved
- simplicity matters

---

## 11. Main unsupervised model families

### Clustering
Examples:
- KMeans
- DBSCAN
- Agglomerative Clustering

Used when:
- you want to find structure without labels
- group discovery matters
- exploratory analysis is part of the task

### Dimensionality reduction
Examples:
- PCA
- TruncatedSVD
- manifold methods such as t-SNE for visualization

Used when:
- you want lower-dimensional representations
- visualization matters
- preprocessing or denoising may help

### Mixture models
Example:
- Gaussian Mixture Models

Used when:
- probabilistic clustering or soft assignment matters

---

## 12. Practical model-selection intuition

A strong practical default for structured/tabular tasks is often to compare a few families:

- a linear baseline
- a tree/forest baseline
- a boosting model
- maybe an SVM or k-NN depending on the problem

This is better than assuming one model family is “the best” in the abstract.

The right question is usually:

> “Which model works best on this dataset under this evaluation setup?”

That is why scikit-learn’s common API and evaluation tools are so valuable.

---

## 13. Why preprocessing still matters

Even though this wiki is not mainly about preprocessing, it is important to say this clearly:

Model performance often depends as much on preprocessing as on the estimator itself.

Examples:
- scaling can matter a lot for SVM and k-NN
- feature representation can transform linear models
- missing-value handling can affect nearly any workflow

This is one reason scikit-learn pipelines are so useful in practice.

---

# Part III — Model Serialization and Basic Inference

## 14. Why persistence matters

Training a model is only one part of the workflow.

If the model is useful, you usually need to:
- save it
- load it later
- use it on new data
- keep preprocessing consistent
- version the artifact

This is where **model serialization** and **basic inference** come in.

---

## 15. What model serialization means

Model serialization means saving the trained model artifact so it can be loaded later without retraining.

The current scikit-learn persistence guide documents several approaches, including `pickle`, `joblib`, `cloudpickle`, `skops.io`, and ONNX for appropriate use cases. citeturn126053search3

### Practical distinction
There are two broad styles here:

#### Python object persistence
Examples:
- `pickle`
- `joblib`
- `cloudpickle`
- `skops.io`

This keeps the model as a Python-side artifact.

#### Interoperable inference format
Example:
- ONNX

This is more about serving/inference portability than preserving a live Python object graph.

---

## 16. Common persistence choices

### `joblib`
A very common practical choice for scikit-learn workflows because it integrates well with standard Python ML artifact saving. The scikit-learn guide still documents it as one of the main persistence options. citeturn126053search3

### `pickle` and `cloudpickle`
Useful in standard Python persistence workflows, but they come with the usual trust and environment caveats.

### `skops.io`
Presented in scikit-learn’s persistence guidance as a more security-conscious alternative in some workflows. citeturn126053search3

### ONNX
Useful when you need serving without reloading the model as a normal Python object and when the model/export path is supported by the relevant tooling. The official persistence guide includes ONNX as one of the decision branches for persistence. citeturn126053search3

---

## 17. Security and compatibility caution

The scikit-learn persistence docs emphasize two important realities:

- persistence methods like pickle-based formats require a compatible environment to reload correctly
- loading pickle-like artifacts from untrusted sources is dangerous because such formats can execute arbitrary code during loading. citeturn126053search3

This means practical persistence strategy is not just “save the file.”

It also means:
- version your environments
- track model metadata
- do not load untrusted artifacts
- save enough context to reproduce the model later

---

## 18. The importance of serializing preprocessing too

A common production mistake is saving only the estimator while forgetting the preprocessing pipeline.

A stronger pattern is to serialize the whole pipeline:
- scaler
- encoder
- feature transformer
- model

That reduces training/serving mismatch.

This is one of the biggest practical wins of scikit-learn’s pipeline model.

---

## 19. What basic inference means

Basic inference means using the trained and loaded model to make predictions on new data.

Typical methods include:
- `predict()`
- `predict_proba()` for supported classifiers
- `decision_function()` for some estimators

Examples of what inference can mean:
- predict a class label
- predict a probability
- predict a numeric regression target

---

## 20. Input discipline for inference

Inference seems simple, but it is fragile if the input does not match training assumptions.

Important practical requirements:
- same feature order
- same preprocessing assumptions
- same data representation
- same expected shape
- same category handling rules

A model that is “correct” can still produce useless predictions if the input schema is wrong.

This is why serialized pipelines and explicit schema handling matter so much.

---

## 21. A practical end-to-end flow

A common real workflow is:

1. load data with pandas or Polars
2. convert or prepare features for modeling
3. train a scikit-learn model
4. serialize the fitted pipeline/model
5. load it later in another process or service
6. run inference on new data

This is the practical bridge from notebooks or experiments to actual use.

---

# Part IV — How the Pieces Fit Together

## 22. A realistic ecosystem path

A realistic Python ML path often looks like this:

### Data representation
Use:
- NumPy for arrays
- pandas for labeled tables
- Polars for performance-oriented table pipelines

### Modeling
Use:
- scikit-learn for classical models on structured data

### Persistence
Use:
- a supported serialization path that matches your deployment needs

### Inference
Use:
- `predict()`-style APIs on validated, correctly shaped new input

This is a coherent workflow, not a random set of libraries.

---

## 23. Choosing tools by problem type

A useful practical summary is:

- use **NumPy** when the problem is fundamentally numerical and array-based
- use **pandas** when the problem is mostly labeled tabular analysis and ecosystem compatibility
- use **Polars** when the problem is tabular and performance/lazy execution matter
- use **scikit-learn** when classical ML on structured data is the goal
- use **serialized pipelines/models** when you need reproducible reuse and deployment

---

## 24. Common mistakes

Some common mistakes across these topics include:

- forcing NumPy into workflows that are really table-analysis problems
- assuming pandas and Polars are interchangeable in style and performance
- choosing models by hype instead of evaluation
- ignoring preprocessing when comparing models
- serializing only the model and not the full transformation pipeline
- loading persisted artifacts without thinking about security or environment compatibility
- sending incorrectly shaped or mismatched data into inference

These mistakes are common because the individual steps seem simple.  
The difficulty appears at the boundaries between them.

---

## 25. Final recommendations

A practical medium-level strategy is:

1. Learn the distinct roles of NumPy, pandas, and Polars.
2. Treat scikit-learn as the main classical ML toolkit for structured data.
3. Start model selection with strong baselines instead of one “fancy” model.
4. Persist the full fitted pipeline when possible, not just the estimator.
5. Be careful with environment compatibility and artifact trust.
6. Treat inference as a contract problem, not just a method call.

When these pieces are handled clearly, Python becomes a very strong environment for structured data and classical machine learning work.

---

## 26. Quick summary

If you only keep the essentials:

- **NumPy** is the array and numeric computation layer. citeturn126053search0turn126053search4
- **pandas** is the labeled tabular analysis layer. citeturn126053search1
- **Polars** is the modern performance-oriented DataFrame layer with strong lazy execution support. citeturn126053search2turn126053search6
- **scikit-learn** organizes classical ML into supervised and unsupervised model families under a common API. citeturn126053search7turn126053search11
- **model persistence** bridges training and deployment, but environment compatibility and artifact trust matter. citeturn126053search3

---
