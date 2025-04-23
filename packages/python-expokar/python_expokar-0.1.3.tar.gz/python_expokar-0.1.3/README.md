# Python Expokar

A comprehensive collection of machine learning algorithm implementations including Logistic Regression, Support Vector Machines (SVM), Neural Networks, Principal Component Analysis (PCA), and more.

## Installation

```bash
pip install python-expokar
```

## Features

- **Linear Regression**: Base, Ridge (L2) and Lasso (L1) implementations
- **Logistic Regression**: Implementation with various regularization options
- **Support Vector Machines**: Implementation with multiple kernel options
- **Neural Networks**: McCulloch-Pitts neuron and Hebbian learning implementations
- **Principal Component Analysis (PCA)**: Dimensionality reduction implementation

## Usage Examples

### Linear Regression
```python
from python_expokar.ml.linear_regression import Ridge, Lasso

# Ridge Regression
ridge_model = Ridge(alpha=1.0)  # L2 regularization strength
ridge_model.fit(X_train, y_train)
ridge_predictions = ridge_model.predict(X_test)

# Lasso Regression
lasso_model = Lasso(alpha=1.0)  # L1 regularization strength
lasso_model.fit(X_train, y_train)
lasso_predictions = lasso_model.predict(X_test)
```

### Logistic Regression
```python
from python_expokar.ml import CustomLogisticRegression

# Create and train the model
model = CustomLogisticRegression(learning_rate=0.01, n_iterations=1000)
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)
```

### Support Vector Machine
```python
from python_expokar.ml import SVM

# Train SVM with different kernels
svm_model = SVM(kernel='rbf', gamma='scale', C=1.0)
svm_model.fit(X_train, y_train)
```

### Neural Networks
```python
from python_expokar.ml import HebbianNeuron

# Create and train a Hebbian neuron
neuron = HebbianNeuron(input_size=2, learning_rate=0.1)
neuron.train_hebbian(X_train, y_train)
```

## Requirements

- Python >= 3.6
- NumPy >= 1.19.0
- scikit-learn >= 0.24.0
- matplotlib >= 3.3.0
- pandas >= 1.2.0
- seaborn >= 0.11.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.