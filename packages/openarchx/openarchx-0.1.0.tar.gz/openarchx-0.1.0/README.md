# OpenArchX

[![PyPI version](https://badge.fury.io/py/openarchx.svg)](https://badge.fury.io/py/openarchx)
[![GitHub license](https://img.shields.io/github/license/openarchx/openarchx)](https://github.com/openarchx/openarchx/blob/main/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/openarchx.svg)](https://pypi.org/project/openarchx/)

A lightweight and extensible deep learning framework in pure Python with native model serialization support.

## Features

- Simple and clean API inspired by modern deep learning frameworks
- Native `.oaxm` model serialization format
- Seamless integration with PyTorch, TensorFlow, and Hugging Face
- Framework-agnostic design for maximum flexibility
- Pure Python implementation with minimal dependencies

## Installation

### Basic Installation

```bash
pip install openarchx
```

### With Framework Integration Support

```bash
# For PyTorch integration
pip install openarchx[pytorch]

# For TensorFlow integration
pip install openarchx[tensorflow]

# For Hugging Face integration
pip install openarchx[huggingface]

# For all integrations
pip install openarchx[all]
```

## Quick Start

```python
import numpy as np
import openarchx as ox
from openarchx.nn import Sequential, Dense, ReLU
from openarchx.core import Tensor
from openarchx.utils import save_model, load_model

# Create a model
model = Sequential([
    Dense(10, input_dim=5),
    ReLU(),
    Dense(1)
])

# Generate dummy data
X = np.random.randn(100, 5).astype(np.float32)
y = np.sum(X * np.array([0.2, 0.5, -0.3, 0.7, -0.1]), axis=1, keepdims=True)
X, y = Tensor(X), Tensor(y)

# Train the model
optimizer = ox.optim.SGD(model.parameters(), learning_rate=0.01)
loss_fn = ox.losses.MSELoss()

for epoch in range(10):
    # Forward pass
    y_pred = model(X)
    loss = loss_fn(y_pred, y)
    
    # Backward pass
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    print(f"Epoch {epoch}: Loss = {loss.data}")

# Save the model to .oaxm format
save_model(model, "my_model.oaxm")

# Load the model
loaded_model = load_model("my_model.oaxm", model_class=Sequential)
```

## Model Serialization with .oaxm

OpenArchX provides a native model serialization format called `.oaxm` (OpenArchX Model):

```python
# Save a model with metadata
metadata = {
    "description": "My trained model",
    "version": "1.0.0",
    "author": "Your Name"
}
save_model(model, "model.oaxm", metadata=metadata)

# Convert from PyTorch
from openarchx.utils import convert_from_pytorch
convert_from_pytorch(torch_model, "converted_model.oaxm")

# Convert from TensorFlow
from openarchx.utils import convert_from_tensorflow
convert_from_tensorflow(tf_model, "converted_model.oaxm")
```

## Framework Integration

### PyTorch Integration

```python
import torch
import torch.nn as nn
from openarchx.utils import get_pytorch_model_adapter

# Convert PyTorch model to OpenArchX
pt_model = nn.Sequential(
    nn.Linear(10, 5),
    nn.ReLU(),
    nn.Linear(5, 1)
)

# Create an adapter to use the PyTorch model in OpenArchX
adapted_model = get_pytorch_model_adapter(pt_model)
output = adapted_model(Tensor(np.random.randn(1, 10)))
```

### TensorFlow Integration

```python
import tensorflow as tf
from openarchx.utils import get_tensorflow_model_adapter

# Use TensorFlow model in OpenArchX
tf_model = tf.keras.Sequential([
    tf.keras.layers.Dense(5, activation='relu', input_shape=(10,)),
    tf.keras.layers.Dense(1)
])

# Create an adapter to use the TensorFlow model in OpenArchX
adapted_model = get_tensorflow_model_adapter(tf_model)
output = adapted_model(Tensor(np.random.randn(1, 10)))
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.