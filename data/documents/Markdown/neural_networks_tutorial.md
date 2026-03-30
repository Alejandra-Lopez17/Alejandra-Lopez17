# Neural Networks Tutorial

## Introduction to Deep Learning

Neural networks are computing systems inspired by biological neural networks. They consist of layers of interconnected nodes (neurons).

## Basic Architecture

### Input Layer
The input layer receives the initial data into the neural network.

### Hidden Layers
Hidden layers process the inputs through weighted connections and activation functions.

### Output Layer
The output layer produces the final prediction or classification.

## Common Activation Functions

1. **ReLU (Rectified Linear Unit)**: `f(x) = max(0, x)`
2. **Sigmoid**: `f(x) = 1 / (1 + e^(-x))`
3. **Tanh**: `f(x) = (e^x - e^(-x)) / (e^x + e^(-x))`

## Training Process

The training of neural networks involves:
- Forward propagation
- Loss calculation
- Backward propagation (backpropagation)
- Weight optimization using gradient descent

## Example: Image Classification

```python
import torch
import torch.nn as nn

class SimpleNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x
```

## Conclusion

Neural networks are fundamental to modern machine learning and deep learning applications.

