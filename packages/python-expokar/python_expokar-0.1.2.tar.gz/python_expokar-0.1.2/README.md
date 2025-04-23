# Python Expokar

A comprehensive collection of machine learning algorithm implementations including Logistic Regression, Support Vector Machines (SVM), Neural Networks, Principal Component Analysis (PCA), and more.

## Installation

```bash
pip install python-expokar
```

## Features

- **Logistic Regression**: Implementation with various regularization options
- **Support Vector Machines**: Implementation with multiple kernel options
- **Neural Networks**: McCulloch-Pitts neuron and Hebbian learning implementations
- **Principal Component Analysis (PCA)**: Dimensionality reduction implementation
- **Ridge and Lasso Regression**: Regularized linear regression implementations

## Usage Examples

### Logistic Regression
```python
from python_expokar.logistic_regression import CustomLogisticRegression

# Create and train the model
model = CustomLogisticRegression(learning_rate=0.01, n_iterations=1000)
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)
```

### Support Vector Machine
```python
from python_expokar.svm import SVM

# Train SVM with different kernels
svm_model = SVM(kernel='rbf', gamma='scale', C=1.0)
svm_model.fit(X_train, y_train)
```

### Neural Networks
```python
from python_expokar.neural_networks import HebbianNeuron

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