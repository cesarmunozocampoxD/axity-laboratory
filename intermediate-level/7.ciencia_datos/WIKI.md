# NumPy, Polars, and pandas

## 1. Goal

This guide explains three of the most important Python data tools:

- **NumPy**
- **Polars**
- **pandas**

It focuses on:

- what each library is for
- their core data models
- where each one fits best
- strengths and trade-offs
- performance and ergonomics
- typical use cases
- how they complement each other

The goal is to help you understand not only what each library does, but also **when you should reach for one instead of another**.

---

## 2. The short intuition

A useful first mental model is:

- **NumPy** → numerical arrays and vectorized numeric computation
- **pandas** → labeled tabular analysis with a very broad ecosystem
- **Polars** → fast DataFrame processing with a modern expression and lazy-execution model

This is not the whole story, but it is a strong starting point.

---

## 3. What NumPy is

**NumPy** is the foundation of numerical computing in Python.

Its core concept is the **`ndarray`**, a multidimensional array that stores items of the same type efficiently in memory.

### Why NumPy matters
NumPy is extremely important because it gives Python:

- efficient array storage
- vectorized operations
- broadcasting
- numerical functions
- a base layer used by many scientific libraries

### In simple terms
If your problem is mostly:
- arrays
- matrices
- vectors
- numerical transformations
- scientific or mathematical computing

NumPy is often the first tool to consider.

---

## 4. The NumPy mental model

Think of NumPy as:

> “Fast array-oriented numeric computation.”

A NumPy array is not just a Python list.

It is:
- typed
- homogeneous
- memory-efficient
- optimized for vectorized operations

This is what gives NumPy much of its speed and scientific value.

---

## 5. Basic NumPy example

```python
import numpy as np

arr = np.array([1, 2, 3, 4])
print(arr * 2)
```

Output:

```python
[2 4 6 8]
```

### Why this matters
The multiplication is applied across the whole array efficiently.

This style is called **vectorized computation**.

---

## 6. NumPy strengths

NumPy is especially strong at:

- numerical arrays
- linear algebra
- vectorized math
- broadcasting
- scientific computing
- interoperability with scientific libraries
- lower-level performance-oriented numeric work in Python

### Good fit
Use NumPy when your data is naturally:
- numeric
- array-shaped
- homogeneous
- computation-heavy

---

## 7. NumPy limitations

NumPy is not primarily designed as a high-level tabular data analysis library.

That means it is less naturally suited for:
- labeled columns
- mixed data types per table
- convenient table joins
- rich tabular groupby workflows
- spreadsheet-like analysis ergonomics

You *can* do a lot with NumPy, but for labeled tabular work, pandas or Polars are usually more natural.

---

## 8. What pandas is

**pandas** is one of the most widely used Python libraries for data analysis and manipulation.

Its central concepts are:

- **Series** → one-dimensional labeled array
- **DataFrame** → two-dimensional labeled table

### In simple terms
Think of pandas as:

> “Flexible, labeled tabular analysis for Python.”

It is especially useful when you want to work with data like:
- CSV files
- spreadsheets
- SQL-like tables
- time series
- business analytics data
- mixed-type datasets

---

## 9. The pandas mental model

pandas is built around **labels** and **tabular workflows**.

That means it is very good at operations like:

- selecting columns by name
- filtering rows
- grouping
- aggregating
- merging
- reshaping
- handling missing values
- time series analysis

If NumPy feels like “array computing,” pandas feels more like:

> “Table-oriented data analysis with labels.”

---

## 10. Basic pandas example

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ana", "Luis", "Sofía"],
    "age": [25, 31, 28]
})

print(df["age"].mean())
```

### Why this is useful
You can work with named columns directly and perform analysis in a very readable way.

---

## 11. pandas strengths

pandas is especially strong at:

- labeled tabular data
- exploratory data analysis
- CSV/Excel/SQL-style workflows
- missing-data handling
- time series
- joins and merges
- grouping and aggregation
- broad ecosystem compatibility

### Good fit
Use pandas when:
- your data feels like a table
- labels matter
- you need flexible analysis
- you need mature ecosystem support
- you want lots of community examples and documentation

---

## 12. pandas limitations

pandas is powerful, but it can become slower or more memory-heavy for some workloads, especially with very large datasets or highly performance-sensitive pipelines.

It is also easy to write pandas code that is:
- convenient
- correct
- but not especially fast

This does not make pandas bad.  
It just means that convenience and flexibility sometimes come with performance trade-offs.

---

## 13. What Polars is

**Polars** is a modern DataFrame library designed for high performance and efficient processing of structured data.

Its core is written in **Rust**, and it supports both:

- **eager** execution
- **lazy** execution

### In simple terms
Think of Polars as:

> “Fast DataFrame processing with a modern, expression-oriented design.”

---

## 14. The Polars mental model

Polars combines tabular analysis with a more query-oriented and optimization-friendly model.

A key concept is the **LazyFrame**:

- operations can be declared first
- execution can be deferred
- the engine can optimize the query plan before running it

This gives Polars a different feel from pandas.

pandas often feels like:
- direct step-by-step table manipulation

Polars often feels more like:
- building a data transformation query plan

---

## 15. Basic Polars example

```python
import polars as pl

df = pl.DataFrame({
    "name": ["Ana", "Luis", "Sofía"],
    "age": [25, 31, 28]
})

result = df.select(pl.col("age").mean())
print(result)
```

### Why this matters
Polars often encourages an expression-based style rather than ad hoc row/column mutation patterns.

---

## 16. Polars lazy execution example

```python
import polars as pl

lf = (
    pl.DataFrame({
        "age": [25, 31, 28, 40]
    })
    .lazy()
    .filter(pl.col("age") > 30)
    .select(pl.col("age").mean())
)

result = lf.collect()
print(result)
```

### Why this is important
The operations are not executed immediately.  
They are collected and optimized before execution.

This is one of the most distinctive features of Polars.

---

## 17. Polars strengths

Polars is especially strong at:

- high-performance DataFrame operations
- large tabular workloads
- expression-based transformation pipelines
- lazy execution
- query optimization
- multi-threaded execution
- modern columnar-style processing patterns

### Good fit
Use Polars when:
- performance matters a lot
- your workload is tabular
- transformations are pipeline-like
- you want lazy query planning
- you want a modern DataFrame API designed with optimization in mind

---

## 18. Polars limitations

Polars is powerful, but some teams may still prefer pandas when:
- they rely on the broader pandas ecosystem
- notebooks or tutorials are heavily pandas-centered
- compatibility with existing codebases matters more than speed
- a library they use expects pandas objects directly

In other words:
Polars is excellent, but ecosystem fit still matters.

---

## 19. Core data model comparison

### NumPy
Core model:
- `ndarray`

Nature:
- homogeneous N-dimensional arrays

Best for:
- numeric and scientific array computation

### pandas
Core models:
- `Series`
- `DataFrame`

Nature:
- labeled one-dimensional and two-dimensional tabular data

Best for:
- flexible tabular analysis

### Polars
Core models:
- `DataFrame`
- `LazyFrame`

Nature:
- expression-oriented tabular processing, eager or lazy

Best for:
- fast tabular transformation pipelines

---

## 20. Homogeneous vs heterogeneous data

This is one of the most important conceptual differences.

### NumPy
Best suited to homogeneous typed arrays.

### pandas
Very comfortable with mixed-type tabular data.

### Polars
Also works naturally with tabular schemas and typed columns, while keeping a stronger performance-oriented design than typical ad hoc pandas workflows.

### Practical takeaway
If your data is fundamentally:
- one numeric array → NumPy is often the natural fit
- one labeled table with mixed columns → pandas or Polars is often more natural

---

## 21. Performance intuition

A useful intuition is:

- **NumPy** is extremely strong for vectorized numerical array math
- **pandas** is often the most flexible and familiar for analysis workflows
- **Polars** often shines in high-performance tabular transformation pipelines

### Important
Real performance depends on:
- workload shape
- data size
- operation types
- memory behavior
- execution style
- library usage style

So performance should be measured in real use cases, not assumed from slogans.

---

## 22. Eager vs lazy execution

This is especially relevant for Polars.

### Eager execution
Operations run immediately.

This is how many pandas workflows feel.

### Lazy execution
Operations are described first, then optimized and executed later.

This is one of Polars’ major strengths.

### Why lazy execution can help
It can allow:
- query optimization
- operation reordering
- reduced unnecessary work
- better end-to-end pipeline performance

---

## 23. Expression style vs imperative style

### pandas
Many workflows feel more imperative and step-by-step.

Example style:
- create a DataFrame
- mutate columns
- filter
- group
- merge
- inspect intermediate objects

### Polars
Often encourages a more expression-based style.

Example style:
- define transformations with expressions
- combine them in a pipeline
- collect at the end

### Why this matters
The coding style feels different, not just the syntax.

---

## 24. Ecosystem position

### NumPy
A foundational building block in scientific Python.

### pandas
A dominant library in data analysis, notebooks, and business/scientific tabular workflows.

### Polars
A newer but very important modern DataFrame option, especially attractive when performance and lazy query planning matter.

### Practical note
Library choice is often influenced not only by features, but also by:
- team familiarity
- codebase history
- ecosystem compatibility
- notebook workflows
- surrounding tooling

---

## 25. Typical use cases for NumPy

Good examples:
- matrix operations
- vectorized numerical simulation
- numerical feature computation
- signal processing
- scientific preprocessing
- lower-level array manipulation
- custom numerical algorithms

If the problem feels mathematical and array-oriented, NumPy is often the right core tool.

---

## 26. Typical use cases for pandas

Good examples:
- reading CSVs and analyzing them
- joining sales/customer/product tables
- cleaning spreadsheet-like datasets
- exploratory analysis in notebooks
- working with missing values
- time series reporting
- generating business summaries

If the problem feels like “data analysis over labeled columns,” pandas is often the default tool.

---

## 27. Typical use cases for Polars

Good examples:
- fast ETL-style transformations
- large tabular processing pipelines
- repeated filter/select/groupby pipelines
- performance-sensitive DataFrame workloads
- data engineering tasks where lazy execution helps
- structured data processing at scale

If the problem feels like “efficient query-like transformations over tables,” Polars becomes especially attractive.

---

## 28. Interoperability mindset

These libraries are not enemies.  
They often complement each other.

A realistic workflow may be:

- use NumPy for numerical arrays
- use pandas for notebook exploration or ecosystem compatibility
- use Polars for fast production transformations

Or:

- use Polars to load and transform data
- convert to pandas when a specific library expects pandas
- convert to NumPy when a numerical model expects arrays

### Practical idea
The right question is often not:
> “Which library is universally best?”

The better question is:
> “Which library fits this part of the workflow best?”

---

## 29. Learning curve intuition

### NumPy
You need to learn:
- arrays
- shapes
- dtypes
- broadcasting
- vectorized thinking

### pandas
You need to learn:
- Series/DataFrame operations
- indexing
- filtering
- groupby
- merge/join
- missing data handling

### Polars
You need to learn:
- expressions
- eager vs lazy modes
- pipeline style
- column expressions
- collect-based execution thinking

Each has its own mental model.  
Polars often feels easiest after you already understand DataFrame workflows conceptually.

---

## 30. Common beginner mistake: using pandas like NumPy

A common mistake is expecting pandas to behave exactly like a simple numeric array tool.

But pandas is more about:
- labels
- alignment
- tabular semantics
- heterogeneous columns

This is powerful, but different from plain numeric array thinking.

---

## 31. Common beginner mistake: using NumPy like a full table library

Another common mistake is trying to force NumPy to behave like a high-level table-analysis framework.

NumPy is excellent, but it is not primarily about:
- column labels
- rich joins
- business-style grouped tables
- spreadsheet-like ergonomics

That is usually where pandas or Polars fit better.

---

## 32. Common beginner mistake: expecting Polars to feel exactly like pandas

Polars has similarities with pandas because both are DataFrame libraries, but the style is not identical.

Polars often pushes you more toward:
- expressions
- column-based transformations
- lazy execution thinking
- pipeline composition

That difference is part of its value.

---

## 33. Choosing by problem type

A simple selection guide:

### Choose NumPy when:
- your data is fundamentally arrays
- the work is numerical
- vectorized math is central
- you care about shapes, broadcasting, and numeric operations

### Choose pandas when:
- your data is tabular and labeled
- flexibility and ecosystem support matter
- you are doing analysis, cleaning, joins, time series, or notebook exploration

### Choose Polars when:
- your data is tabular
- performance matters strongly
- transformation pipelines are central
- lazy execution and query optimization are useful

---

## 34. Pythonic examples side by side

### NumPy

```python
import numpy as np

arr = np.array([1, 2, 3])
print(arr + 10)
```

### pandas

```python
import pandas as pd

df = pd.DataFrame({"x": [1, 2, 3]})
print(df["x"] + 10)
```

### Polars

```python
import polars as pl

df = pl.DataFrame({"x": [1, 2, 3]})
print(df.select(pl.col("x") + 10))
```

### Why this comparison helps
The same conceptual operation exists in all three, but the mental model and API style differ.

---

## 35. Data size and workflow shape

Tool choice is often influenced by both:
- **data size**
- **workflow shape**

### Smaller and exploratory
pandas is often very comfortable.

### Numerical core arrays
NumPy is often ideal.

### Larger, pipeline-heavy, performance-sensitive tables
Polars often becomes very attractive.

This is a practical rather than ideological decision.

---

## 36. Common mistakes

### 1. Choosing only by hype
The best library depends on the workload.

### 2. Using NumPy for problems that are really table-analysis problems
This often creates unnecessary complexity.

### 3. Using pandas for very large performance-critical pipelines without measuring alternatives
Convenience is great, but performance should be measured.

### 4. Using Polars without adapting to its expression/lazy model
Treating it as “just pandas with different names” misses much of its value.

### 5. Looking for one universal winner
These libraries solve overlapping but not identical problems.

---

## 37. Best practices

### 1. Start from the data model
Ask whether the problem is:
- array-oriented
- table-oriented
- lazily transform-oriented

### 2. Match the tool to the workflow
Exploration, production ETL, and numerical computing may benefit from different tools.

### 3. Measure performance in real workloads
Do not rely only on general claims.

### 4. Learn the mental model, not just syntax
Each library has a way of thinking:
- arrays for NumPy
- labeled tables for pandas
- expressions and lazy pipelines for Polars

### 5. Use interoperability pragmatically
You do not have to choose one tool forever.

---

## 38. Practical mental model

A useful mental model is:

- **NumPy** → “Compute on arrays.”
- **pandas** → “Analyze labeled tables.”
- **Polars** → “Transform tables efficiently with expressions and lazy execution.”

That alone will already help with many library decisions.

---

## 39. Final recommendation

A practical default approach is:

- reach for **NumPy** when the work is fundamentally numerical and array-based
- reach for **pandas** when you need flexible labeled tabular analysis and strong ecosystem compatibility
- reach for **Polars** when you want a modern, high-performance DataFrame engine with strong support for expression-based and lazy workflows

The best choice is not about loyalty to one library.  
It is about choosing the right abstraction for the shape of the problem.

---

## 40. Quick summary

If you only keep the essentials:

1. NumPy is the core array library for numerical computing in Python.
2. pandas is the most established labeled tabular analysis library in Python.
3. Polars is a fast modern DataFrame library with eager and lazy execution modes.
4. NumPy fits array-heavy numeric work, pandas fits flexible labeled table workflows, and Polars fits fast query-like tabular pipelines.
5. These libraries often complement each other rather than replace each other completely.

---

# scikit-learn: Classical Models

## 1. Goal

This guide explains the main **classical machine learning model families** in **scikit-learn**.

It focuses on:

- what “classical models” means
- the main supervised model families
- the main unsupervised model families
- when each family is useful
- strengths and limitations
- practical intuition for choosing among them

The goal is not to memorize every estimator in the library.  
The goal is to build a clear mental map of the most important traditional models available in scikit-learn.

---

## 2. What “classical models” means here

In this guide, **classical models** means the model families that are traditionally associated with standard machine learning before modern deep learning became the default for many tasks.

These usually include:

- linear models
- logistic regression
- support vector machines
- k-nearest neighbors
- decision trees
- random forests
- gradient boosting
- naive Bayes
- clustering methods
- dimensionality reduction methods
- Gaussian mixture models

### Important
These models are still very important.

They are often:
- strong baselines
- easier to train
- easier to interpret
- effective on tabular data
- cheaper to run than deep learning approaches

---

## 3. Why classical models still matter

Classical models remain highly useful because they are often:

- faster to train
- easier to debug
- easier to explain
- strong on structured/tabular data
- effective with smaller datasets
- easier to deploy in many business settings

A lot of real-world machine learning work still relies on these models.

---

## 4. scikit-learn’s role

scikit-learn is one of the most important Python libraries for classical machine learning.

It gives a common API for:

- training estimators
- making predictions
- preprocessing
- model selection
- evaluation
- pipelines
- feature engineering helpers

### Common API pattern
Most estimators follow the same style:

```python
model.fit(X_train, y_train)
preds = model.predict(X_test)
```

This consistency is one of the reasons scikit-learn is so widely used.

---

## 5. Main categories

A useful first classification is:

### Supervised learning
You have input data `X` and known targets `y`.

Common tasks:
- classification
- regression

### Unsupervised learning
You have input data `X` but no target labels.

Common tasks:
- clustering
- dimensionality reduction
- density modeling
- anomaly detection

---

# Supervised Models

## 6. Linear models

Linear models are among the most important classical models.

For regression, common examples include:
- Linear Regression
- Ridge
- Lasso
- Elastic Net

For classification, a key example is:
- Logistic Regression

### Main intuition
A linear model tries to explain the prediction using a weighted combination of input features.

---

## 7. Linear Regression

**Linear Regression** is the standard baseline model for regression.

### Best for
- simple regression baselines
- relationships that are roughly linear
- interpretable coefficient-based modeling

### Strengths
- simple
- fast
- interpretable
- strong baseline

### Limitations
- limited for nonlinear relationships unless features are engineered
- sensitive to multicollinearity and outliers in many settings

### Example

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
preds = model.predict(X_test)
```

---

## 8. Ridge, Lasso, and Elastic Net

These are regularized linear models.

### Ridge
Adds L2 regularization.

Good when:
- many features contribute a little
- you want coefficient shrinkage
- overfitting is a concern

### Lasso
Adds L1 regularization.

Good when:
- you want sparsity
- some features may be irrelevant
- feature selection pressure is useful

### Elastic Net
Combines L1 and L2.

Good when:
- you want a balance between shrinkage and sparsity

### Practical note
These are often stronger real-world choices than plain linear regression when features are numerous or noisy.

---

## 9. Logistic Regression

Despite its name, **Logistic Regression** is a classification model.

### Best for
- binary classification
- multiclass classification in many practical cases
- interpretable baselines
- linearly separable or approximately separable problems

### Strengths
- simple
- fast
- often surprisingly strong on tabular data
- probabilistic outputs
- interpretable coefficients

### Limitations
- still fundamentally linear in decision boundary unless features are transformed
- may underperform on strongly nonlinear data

### Example

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
preds = model.predict(X_test)
```

---

## 10. Support Vector Machines (SVM)

Support Vector Machines are a major classical model family.

Common estimators include:
- `SVC`
- `SVR`
- `LinearSVC`
- `LinearSVR`

### Main intuition
SVMs try to separate data with a margin, and kernelized variants can model nonlinear boundaries.

---

## 11. When SVMs are useful

SVMs are often useful when:
- the dataset is not huge
- decision boundaries are not trivially linear
- feature spaces may be high-dimensional
- you want a strong classical classifier baseline

### Strengths
- can be very strong in classification
- kernel trick enables nonlinear separation
- works well in many medium-sized problems

### Limitations
- can be slower on large datasets
- parameter tuning matters a lot
- probabilistic outputs are less direct than some other models
- scaling can become painful for very large workloads

### Example

```python
from sklearn.svm import SVC

model = SVC()
model.fit(X_train, y_train)
preds = model.predict(X_test)
```

---

## 12. k-Nearest Neighbors (k-NN)

k-NN is one of the simplest classical models.

### Main intuition
To predict for a new point, look at the nearest training points and infer from them.

For classification:
- nearby class labels vote

For regression:
- nearby target values are averaged

---

## 13. When k-NN is useful

k-NN is useful when:
- you want a simple baseline
- local similarity is meaningful
- the dataset is not too large
- feature scaling can be handled properly

### Strengths
- easy to understand
- almost no training in the usual sense
- flexible nonlinear behavior

### Limitations
- prediction can be slow
- sensitive to feature scaling
- degrades in high dimensions
- memory-heavy because it keeps the training data

### Example

```python
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
preds = model.predict(X_test)
```

---

## 14. Decision Trees

Decision trees split the feature space into regions using learned decision rules.

### Main intuition
A tree repeatedly asks questions like:

- is feature A less than threshold T?
- if yes, go left
- if no, go right

until it reaches a prediction.

---

## 15. When Decision Trees are useful

Decision trees are useful when:
- interpretability matters
- nonlinear relationships exist
- feature interactions matter
- you want a model that handles mixed feature patterns more flexibly than linear models

### Strengths
- interpretable
- handles nonlinear relationships
- captures interactions automatically
- requires less feature scaling than distance-based models

### Limitations
- prone to overfitting
- unstable to small data changes
- often weaker alone than ensemble versions

### Example

```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(max_depth=5)
model.fit(X_train, y_train)
preds = model.predict(X_test)
```

---

## 16. Random Forests

Random Forests are ensembles of decision trees.

### Main intuition
Instead of relying on one potentially unstable tree, build many trees and aggregate them.

For classification:
- majority vote

For regression:
- average predictions

---

## 17. When Random Forests are useful

Random Forests are often useful when:
- you need a strong tabular baseline
- relationships are nonlinear
- you want less overfitting than a single tree
- interpretability matters somewhat, but not as strictly as with one tree

### Strengths
- strong on tabular data
- robust baseline
- handles nonlinearities and interactions
- less fragile than a single tree
- often works well with relatively little tuning

### Limitations
- less interpretable than a single tree
- can be heavier than linear models
- may not be as strong as more advanced boosting methods in some structured problems

### Example

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)
preds = model.predict(X_test)
```

---

## 18. Gradient Boosting and boosting-style ensembles

Boosting methods build models sequentially, where each new model tries to correct previous errors.

In scikit-learn, key families include:
- Gradient Boosting
- HistGradientBoosting

### Main intuition
Instead of averaging many independent trees like Random Forest, boosting builds a sequence of trees that improve the residual mistakes.

---

## 19. When boosting is useful

Boosting is often useful when:
- tabular predictive performance matters strongly
- nonlinear structure exists
- you want more predictive power than simpler baselines

### Strengths
- often very strong on tabular data
- captures nonlinear patterns
- often competitive with many advanced methods on structured datasets

### Limitations
- more tuning-sensitive than simpler baselines
- can overfit if configured poorly
- less interpretable than linear models and simple trees

### Example

```python
from sklearn.ensemble import HistGradientBoostingClassifier

model = HistGradientBoostingClassifier()
model.fit(X_train, y_train)
preds = model.predict(X_test)
```

---

## 20. Naive Bayes

Naive Bayes models are probabilistic classifiers based on Bayes’ theorem with strong feature-independence assumptions.

Common scikit-learn variants include:
- GaussianNB
- MultinomialNB
- BernoulliNB
- ComplementNB
- CategoricalNB

---

## 21. When Naive Bayes is useful

Naive Bayes is useful when:
- you need a fast baseline
- data is text-like or count-based, especially for MultinomialNB
- simplicity matters
- the independence assumption is acceptable enough to still work well

### Strengths
- very fast
- simple
- often surprisingly effective for text classification
- works well as a baseline

### Limitations
- assumptions can be unrealistic
- may underperform more flexible models on many structured problems

### Example

```python
from sklearn.naive_bayes import MultinomialNB

model = MultinomialNB()
model.fit(X_train, y_train)
preds = model.predict(X_test)
```

---

## 22. Neural network models in scikit-learn

scikit-learn also includes classical feedforward neural network estimators such as:
- `MLPClassifier`
- `MLPRegressor`

### Important framing
These are neural network models, but in scikit-learn they usually play the role of classical ML estimators rather than full modern deep learning frameworks.

### Best for
- medium-scale structured problems
- experiments where you want an MLP inside the scikit-learn API

### Limitation
For serious modern deep learning workloads, people usually move to frameworks like PyTorch or TensorFlow instead.

---

# Unsupervised Models

## 23. Clustering

Clustering tries to group data points without labeled targets.

Common scikit-learn clustering methods include:
- KMeans
- Agglomerative Clustering
- DBSCAN
- HDBSCAN
- OPTICS
- Spectral Clustering
- Birch

### Main intuition
The model tries to discover structure or grouping patterns in the data.

---

## 24. KMeans

KMeans is one of the most common clustering algorithms.

### Main intuition
It partitions the data into `k` clusters by assigning points to the nearest cluster center and iteratively refining those centers.

### Strengths
- simple
- fast
- widely understood
- strong baseline for clustering

### Limitations
- requires you to choose `k`
- works best with roughly spherical clusters
- sensitive to scaling and initialization
- not ideal for irregular cluster shapes

### Example

```python
from sklearn.cluster import KMeans

model = KMeans(n_clusters=3, random_state=42)
labels = model.fit_predict(X)
```

---

## 25. DBSCAN and density-based clustering

DBSCAN is a density-based clustering method.

### Main intuition
Clusters are dense regions separated by sparse regions.

### Strengths
- can find irregularly shaped clusters
- does not require specifying number of clusters directly
- can identify noise/outliers

### Limitations
- parameter choice matters a lot
- can struggle when cluster densities differ significantly
- sensitive to feature scaling

### Example

```python
from sklearn.cluster import DBSCAN

model = DBSCAN(eps=0.5, min_samples=5)
labels = model.fit_predict(X)
```

---

## 26. Hierarchical / Agglomerative clustering

Agglomerative clustering builds clusters bottom-up by merging nearby groups.

### Strengths
- useful when hierarchy is meaningful
- can be more flexible than KMeans in cluster structure
- dendrogram-style interpretation can be valuable conceptually

### Limitations
- can be heavier computationally
- still depends on linkage and distance choices

---

## 27. Gaussian Mixture Models (GMM)

Gaussian Mixture Models model the data as a mixture of Gaussian distributions.

### Main intuition
Instead of hard assigning each point to a single cluster, GMM can model soft probabilistic cluster membership.

### Strengths
- probabilistic clustering
- more flexible than KMeans in some distributions
- useful when soft assignments matter

### Limitations
- assumes Gaussian mixture structure
- can be sensitive to initialization and model assumptions

### Example

```python
from sklearn.mixture import GaussianMixture

model = GaussianMixture(n_components=3, random_state=42)
model.fit(X)
labels = model.predict(X)
```

---

## 28. Dimensionality reduction

Dimensionality reduction reduces the number of features while trying to preserve useful structure.

Important scikit-learn methods include:
- PCA
- TruncatedSVD
- NMF
- manifold learning methods such as t-SNE and Isomap

### Why useful
These methods help with:
- visualization
- compression
- denoising
- preprocessing before supervised learning

---

## 29. PCA

Principal Component Analysis (PCA) is one of the most important classical unsupervised methods.

### Main intuition
It finds directions of maximum variance and projects data into a lower-dimensional space.

### Strengths
- standard baseline for dimensionality reduction
- useful for visualization
- useful for preprocessing
- can reduce redundancy in correlated features

### Limitations
- linear method
- transformed components can be harder to interpret directly
- not ideal for all nonlinear structures

### Example

```python
from sklearn.decomposition import PCA

model = PCA(n_components=2)
X_reduced = model.fit_transform(X)
```

---

## 30. t-SNE and manifold-style visualization methods

t-SNE is often used for visualizing high-dimensional data in 2D or 3D.

### Strengths
- very useful for visualization of local structure
- often reveals cluster-like patterns visually

### Limitations
- mostly a visualization tool, not a general-purpose feature reducer
- can be slow
- results depend strongly on settings
- should be interpreted carefully

### Practical note
t-SNE is often used for exploration, not as a default production feature-engineering step.

---

## 31. Outlier and novelty detection

scikit-learn also includes classical methods for anomaly-style tasks, such as:
- OneClassSVM
- IsolationForest
- LocalOutlierFactor

### Why these matter
These methods are useful when the goal is:
- detect unusual observations
- flag anomalies
- separate normal patterns from rare behavior

This is not exactly the same as standard classification or clustering, but it belongs to the broader classical model landscape.

---

# Model choice intuition

## 32. Strong baselines for classification

A useful practical mental map for classification:

- **Logistic Regression** → simple, interpretable, strong baseline
- **Random Forest** → strong nonlinear tabular baseline
- **Gradient Boosting / HistGradientBoosting** → often very strong on tabular tasks
- **SVM** → strong classical classifier, especially for moderate-size problems
- **Naive Bayes** → very fast baseline, especially for text-like settings
- **k-NN** → simple local-similarity baseline

---

## 33. Strong baselines for regression

A useful practical mental map for regression:

- **Linear Regression / Ridge / Lasso / Elastic Net** → first interpretable baselines
- **Decision Tree Regressor** → simple nonlinear regression
- **Random Forest Regressor** → strong tabular nonlinear baseline
- **Gradient Boosting / HistGradientBoosting Regressor** → often strong predictive choice
- **SVR** → strong but can be heavier and more tuning-sensitive

---

## 34. Strong baselines for clustering and structure discovery

A useful practical mental map:

- **KMeans** → simplest clustering baseline
- **DBSCAN** → density-based clustering with noise handling
- **Agglomerative Clustering** → hierarchy-aware clustering
- **GaussianMixture** → soft probabilistic clustering
- **PCA** → first baseline for dimensionality reduction
- **t-SNE** → exploratory visualization tool

---

## 35. Choosing by data type and workflow

### Mostly numeric tabular classification/regression
Start with:
- Logistic Regression
- Random Forest
- Gradient Boosting / HistGradientBoosting

### Text classification with count or tf-idf features
Start with:
- Logistic Regression
- Linear SVM
- MultinomialNB

### Small interpretable baseline
Start with:
- Linear models
- shallow trees

### Unsupervised exploratory clustering
Start with:
- KMeans
- DBSCAN

### Feature compression or visualization
Start with:
- PCA
- then maybe t-SNE for visual exploration

---

## 36. Preprocessing matters a lot

Model performance is not only about the estimator.

Preprocessing can matter as much or more.

Examples:
- scaling for SVM and k-NN
- encoding for categorical features
- missing-value handling
- feature engineering
- dimensionality reduction
- train/test splitting discipline

### Practical lesson
Do not compare models fairly without also considering preprocessing.

---

## 37. Pipelines matter

A very important scikit-learn concept is the **Pipeline**.

Why?
Because real workflows often involve:
- preprocessing
- feature transformation
- estimator fitting

Pipelines help keep that process:
- clean
- reproducible
- less error-prone
- safer during cross-validation

Example:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000))
])

pipe.fit(X_train, y_train)
preds = pipe.predict(X_test)
```

---

## 38. Evaluation matters more than model hype

A common beginner mistake is asking:

> “Which classical model is best?”

The answer depends on:
- data size
- feature quality
- target type
- class balance
- noise
- preprocessing
- metric choice

### Better question
Ask:
- which models are strong baselines for this kind of problem?
- what metric matters?
- what does cross-validation show?

---

## 39. Common mistakes

### 1. Choosing a model by reputation alone
A “fancier” model is not always better.

### 2. Skipping preprocessing
Many models depend heavily on scaling and feature preparation.

### 3. Ignoring baseline models
Simple models can be surprisingly strong.

### 4. Comparing models without proper validation
This leads to misleading conclusions.

### 5. Using t-SNE as if it were a general-purpose modeling step
It is mainly a visualization tool.

### 6. Assuming one model family wins all tabular problems
Model performance depends on the dataset and workflow.

---

## 40. Best practices

### 1. Start with a few strong baselines
Do not jump directly to one complicated model.

### 2. Use pipelines
This makes preprocessing and modeling safer.

### 3. Choose metrics intentionally
Accuracy is not always enough.

### 4. Cross-validate
One split is rarely enough for robust comparison.

### 5. Prefer interpretable baselines early
They help you understand the problem.

### 6. Let experiments decide
Classical model choice should be empirical, not ideological.

---

## 41. Practical mental model

A useful mental model is:

- **linear models** → simple and interpretable
- **SVM / k-NN** → strong classical alternatives with different assumptions
- **trees / forests / boosting** → strong nonlinear tabular models
- **naive Bayes** → very fast probabilistic baselines
- **clustering** → structure without labels
- **PCA and related methods** → lower-dimensional structure and visualization

That is enough to navigate a lot of scikit-learn work effectively.

---

## 42. Final recommendation

When learning scikit-learn classical models, a practical study order is often:

1. Linear Regression and Logistic Regression
2. k-NN
3. Decision Trees
4. Random Forests
5. Gradient Boosting / HistGradientBoosting
6. SVM
7. Naive Bayes
8. KMeans and DBSCAN
9. PCA and Gaussian Mixture Models

This order gives you:
- core supervised baselines
- strong tabular models
- major unsupervised tools
- a good practical mental map

---

## 43. Quick summary

If you only keep the essentials:

1. scikit-learn classical models cover major supervised and unsupervised ML families.
2. Linear models are the main interpretable baselines.
3. Trees, forests, and boosting are powerful tabular nonlinear models.
4. SVM, k-NN, and naive Bayes are important classical alternatives.
5. KMeans, DBSCAN, PCA, and Gaussian Mixture Models are key classical unsupervised tools.

---
# Model Serialization and Basic Inference

## 1. Goal

This guide explains two very practical machine learning topics:

- **model serialization**
- **basic inference**

It focuses mainly on Python workflows, especially with **scikit-learn-style models**, but the ideas also apply more broadly.

The main goals are:

- understanding what serialization means
- knowing common ways to save and load models
- understanding trade-offs between formats
- performing basic inference correctly
- avoiding common production mistakes

---

## 2. What model serialization means

**Model serialization** means saving a trained model to disk so it can be loaded later without retraining.

In simple terms, it answers:

> “How do I keep the trained model and use it again later?”

Typical reasons to serialize a model:
- avoid retraining every time
- deploy the model to another environment
- ship the model to a service or API
- reuse the model in notebooks, scripts, or apps
- persist a pipeline after training

---

## 3. Why serialization matters

Training is often expensive in either:
- time
- compute
- data preparation effort
- tuning effort

If you do not persist the trained artifact, you may have to repeat all of that work just to make predictions again.

Serialization is therefore a key bridge between:
- training
- evaluation
- deployment
- production inference

---

## 4. Serialization vs inference

These two concepts are related but different.

### Serialization
Saving and loading the trained model artifact.

### Inference
Using the trained model to make predictions on new data.

A common workflow is:

1. train the model
2. serialize the model
3. load the model later
4. run inference on new inputs

---

## 5. Basic scikit-learn workflow

A typical training workflow looks like this:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000))
])

pipeline.fit(X_train, y_train)
```

After training, the pipeline can be serialized and reused for inference.

### Why serializing the pipeline is important
If preprocessing is part of the training flow, you usually want to save:
- the preprocessing
- the model

together in one artifact.

That avoids training/serving mismatch.

---

## 6. Common Python serialization options

In Python ML workflows, common serialization choices include:

- `pickle`
- `joblib`
- `cloudpickle`
- `skops.io`
- ONNX for supported export scenarios

Each one has different trade-offs.

---

## 7. `pickle`

`pickle` is Python’s built-in object serialization mechanism.

Example:

```python
import pickle

with open("model.pkl", "wb") as f:
    pickle.dump(pipeline, f)
```

Loading:

```python
import pickle

with open("model.pkl", "rb") as f:
    model = pickle.load(f)
```

### Why it is used
- built into Python
- simple
- familiar
- works for many Python objects

### Main caution
`pickle` loads Python objects by executing object reconstruction logic, so it should not be used to load artifacts from untrusted sources.

---

## 8. `joblib`

`joblib` is very common for scikit-learn model persistence.

Example:

```python
import joblib

joblib.dump(pipeline, "model.joblib")
```

Loading:

```python
import joblib

model = joblib.load("model.joblib")
```

### Why `joblib` is popular
It is often convenient for:
- scikit-learn estimators
- larger arrays
- standard model persistence workflows

### Important
Security concerns are still similar to pickle-based loading in general.  
Do not load untrusted files.

---

## 9. `cloudpickle`

`cloudpickle` can serialize a wider range of Python objects than standard pickle in some cases.

Example:

```python
import cloudpickle

with open("model.cloudpkl", "wb") as f:
    cloudpickle.dump(pipeline, f)
```

Loading:

```python
import cloudpickle

with open("model.cloudpkl", "rb") as f:
    model = cloudpickle.load(f)
```

### Why useful
It can help when your pipeline contains:
- custom functions
- lambdas
- more dynamic Python objects

### Caution
It still shares the general trust/security concerns of pickle-style loading.

---

## 10. `skops.io`

`skops.io` is a more security-conscious persistence option in the scikit-learn ecosystem.

Example:

```python
import skops.io as sio

sio.dump(pipeline, "model.skops")
```

Loading:

```python
import skops.io as sio

model = sio.load("model.skops", trusted=True)
```

### Why it matters
It is designed to offer a safer alternative to plain pickle-style persistence for scikit-learn objects.

### Important note
It is still something you should use thoughtfully, but it is specifically meant to improve the persistence story when security concerns exist.

---

## 11. ONNX

**ONNX** is a model representation format aimed at interoperable inference.

It is not “just another pickle replacement.”  
It is more like:

> “Export the model into a standardized inference graph format.”

### Why ONNX matters
It can be useful when:
- you want serving without Python object loading
- you want a smaller runtime environment
- you want cross-platform inference
- you want to run supported models in ONNX Runtime

### Important
Not every scikit-learn model is supported equally for ONNX conversion.

---

## 12. Basic ONNX export idea

For supported scikit-learn models, a conversion flow may look like:

```python
from skl2onnx import to_onnx
import numpy as np

sample_input = X_train[:1].astype(np.float32)
onnx_model = to_onnx(pipeline, sample_input)
```

Saving:

```python
with open("model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())
```

### Why this is different
You are exporting to an inference format, not storing a Python object graph directly.

---

## 13. ONNX inference idea

Example with ONNX Runtime:

```python
import onnxruntime as ort
import numpy as np

session = ort.InferenceSession("model.onnx")
input_name = session.get_inputs()[0].name

preds = session.run(None, {input_name: X_test.astype(np.float32)})
```

### Why useful
Inference can happen without reloading the original Python estimator object.

---

## 14. How to choose a serialization format

A useful practical decision guide is:

### Use `joblib`
when:
- you are in a standard scikit-learn Python workflow
- you trust the artifact source
- you want simple persistence and loading

### Use `pickle`
when:
- you need basic built-in Python serialization
- the workflow is simple
- you trust the artifact source

### Use `cloudpickle`
when:
- you need broader Python object support
- custom callables or dynamic objects matter

### Use `skops.io`
when:
- you want a more security-conscious persistence option in the scikit-learn ecosystem

### Use ONNX
when:
- you want Python-free or more portable serving
- your model is supported
- inference portability matters more than preserving the full original Python object

---

## 15. Version compatibility matters

One of the biggest real-world issues with model serialization is **environment compatibility**.

A saved model may depend on:
- Python version
- scikit-learn version
- NumPy version
- scipy version
- preprocessing code
- custom class definitions

### Practical rule
A model artifact is usually safest when loaded in an environment that closely matches the one used to create it.

---

## 16. Why reproducibility metadata matters

Saving only the artifact is often not enough.

A serious workflow should usually also store:
- library versions
- training code version
- feature list
- preprocessing details
- label mapping
- training data reference or snapshot reference
- evaluation metrics
- creation date
- model version identifier

### Why this matters
Without metadata, it becomes much harder to:
- reproduce results
- debug production issues
- validate whether the right model is deployed

---

## 17. A practical save package structure

A common production-friendly structure might be:

```text
model_bundle/
├── model.joblib
├── metadata.json
├── feature_names.json
└── README.md
```

Possible metadata content:
- model version
- training date
- library versions
- expected input schema
- target labels
- performance summary

### Why useful
The model artifact becomes much easier to govern and support.

---

## 18. Basic inference

**Inference** means using the trained model to predict on new input data.

Basic example:

```python
preds = model.predict(X_new)
```

This is the simplest case.

---

## 19. Classification inference basics

For classification models, common methods include:

- `predict()`
- `predict_proba()`
- `decision_function()` for some estimators

### `predict()`
Returns final predicted class labels.

```python
pred_labels = model.predict(X_new)
```

### `predict_proba()`
Returns class probabilities for models that support it.

```python
pred_probs = model.predict_proba(X_new)
```

### Why probabilities matter
They are useful when:
- confidence matters
- thresholds need tuning
- ranking matters
- calibration matters

---

## 20. Regression inference basics

For regression models, basic inference usually means:

```python
pred_values = model.predict(X_new)
```

The output is typically numeric predicted values.

Examples:
- predicted price
- predicted demand
- predicted risk score
- predicted duration

---

## 21. Input shape matters

One very common source of errors in inference is incorrect input shape.

Many scikit-learn models expect a 2D array shape:

```python
(n_samples, n_features)
```

### Example
Even for one row, you often still need:

```python
sample = [[5.1, 3.5, 1.4, 0.2]]
pred = model.predict(sample)
```

not:

```python
sample = [5.1, 3.5, 1.4, 0.2]
```

depending on the estimator and API expectations.

---

## 22. Feature order matters

A very important production rule:

> The features used at inference time must match the features used during training.

That includes:
- same order
- same meaning
- same preprocessing assumptions
- same encoding logic
- same scaling logic when relevant

### Why this is critical
A perfectly working model can produce useless predictions if the input feature mapping is wrong.

---

## 23. Pipelines make inference safer

Using a scikit-learn `Pipeline` is often one of the best ways to reduce training/inference mismatch.

Example:

```python
preds = pipeline.predict(X_new)
```

### Why this is safer
The same fitted preprocessing steps are applied automatically before prediction.

This is much safer than manually remembering:
- scaling
- encoding
- transformation steps
- feature engineering order

---

## 24. Single prediction example

```python
sample = [[42, 1, 0.87]]
pred = model.predict(sample)
print(pred)
```

### Why this matters
Single-sample inference is common in APIs and applications, but it still must respect the same shape and feature schema as training.

---

## 25. Batch inference example

```python
samples = [
    [42, 1, 0.87],
    [35, 0, 0.42],
    [29, 1, 0.63],
]

preds = model.predict(samples)
print(preds)
```

### Why batch inference matters
Batch inference is common for:
- reporting
- ETL scoring
- scheduled jobs
- offline evaluation
- bulk prediction pipelines

---

## 26. Basic API-style inference flow

A typical application flow may be:

1. receive raw input
2. validate input schema
3. convert to model input shape
4. call `predict()` or `predict_proba()`
5. post-process output
6. return response

### Why validation matters
Model inference is fragile when:
- fields are missing
- types are wrong
- feature order is inconsistent
- values are out of expected range

---

## 27. Post-processing predictions

Inference is often not just raw model output.

You may also need:
- thresholding probabilities
- mapping class indices to labels
- rounding regression outputs
- applying business rules
- attaching explanation metadata
- formatting JSON responses

### Example

```python
prob = model.predict_proba(sample)[0][1]
label = "positive" if prob >= 0.7 else "negative"
```

### Why this matters
Serving logic often includes a decision layer on top of raw inference.

---

## 28. Latency vs throughput

When thinking about inference in production, two important ideas are:

### Latency
How long one prediction request takes.

### Throughput
How many predictions can be processed over time.

### Why this matters
A model can be good at:
- low-latency single predictions
- or high-throughput batch scoring

but the operational design may differ.

---

## 29. Inference and determinism

Basic inference should usually be deterministic for the same:
- model artifact
- input
- environment assumptions

If predictions change unexpectedly, possible causes include:
- artifact mismatch
- preprocessing mismatch
- version mismatch
- hidden randomness in pipeline steps
- differences in floating-point/runtime environment

---

## 30. Common serialization mistakes

### 1. Loading untrusted pickle/joblib artifacts
This is a serious security mistake.

### 2. Saving only the model and not the preprocessing
This often causes training/serving mismatch.

### 3. Ignoring version compatibility
The artifact may fail or behave unexpectedly in a different environment.

### 4. Not storing feature schema information
This makes inference fragile.

### 5. Using ONNX without checking model support
Not every estimator or pipeline converts cleanly.

---

## 31. Common inference mistakes

### 1. Wrong input shape
Single-row prediction often fails for shape reasons.

### 2. Wrong feature order
This can silently corrupt predictions.

### 3. Missing preprocessing
Manual inference often forgets scaling, encoding, or feature engineering.

### 4. Treating probabilities like labels
`predict_proba()` and `predict()` are not the same.

### 5. No input validation
Bad inputs can lead to crashes or misleading outputs.

---

## 32. Best practices

### 1. Serialize the full pipeline when possible
This reduces mismatch risk.

### 2. Keep metadata with the artifact
Store schema, versions, and model identifiers.

### 3. Trust boundaries matter
Do not load pickle-style artifacts from untrusted sources.

### 4. Validate inference inputs
Check shape, types, required fields, and allowed ranges.

### 5. Use explicit versioning
Treat models as versioned artifacts, not as loose files.

### 6. Test serialization round-trips
Make sure save → load → predict works before deployment.

### 7. Test inference with representative real samples
Not just toy examples.

---

## 33. Practical mental model

A useful mental model is:

- **serialization** = saving the trained predictive artifact safely and reproducibly
- **loading** = reconstructing the model in a compatible environment
- **inference** = sending correctly shaped, correctly preprocessed new data through that model

If any of those three layers is weak, production prediction quality becomes fragile.

---

## 34. A simple end-to-end example with `joblib`

```python
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# Train
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000))
])

pipeline.fit(X_train, y_train)

# Save
joblib.dump(pipeline, "model.joblib")

# Load
loaded_model = joblib.load("model.joblib")

# Inference
preds = loaded_model.predict(X_test)
```

### Why this is a strong baseline pattern
It is:
- simple
- standard
- practical
- relatively easy to productionize

as long as the environment and trust assumptions are controlled.

---

## 35. Final recommendation

A practical default for many Python ML workflows is:

- train a pipeline
- save it with `joblib` in trusted internal environments
- store metadata alongside it
- validate inputs carefully at inference time
- consider `skops.io` when safer persistence is important
- consider ONNX when portable Python-free inference is a real requirement

This gives a solid baseline for moving from training to real prediction use.

---

## 36. Quick summary

If you only keep the essentials:

1. Model serialization means saving a trained model so it can be loaded later without retraining.
2. Common Python options include pickle, joblib, cloudpickle, skops.io, and ONNX for supported export scenarios.
3. Pickle-style formats are convenient but should never be loaded from untrusted sources.
4. Basic inference usually means calling `predict()` or `predict_proba()` on correctly shaped, correctly preprocessed inputs.
5. The safest real-world pattern is often to serialize the full preprocessing + model pipeline and keep schema/version metadata next to it.

---
