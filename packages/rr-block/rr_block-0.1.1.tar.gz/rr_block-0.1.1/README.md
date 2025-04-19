# Remix and Reactivate (RR)

The remix and reactivate (RR) Block official implementation for PyTorch.

## Installation

You can install this package using pip:

```bash
pip install rr-block
```

## Usage
Here is a simple example of how to use the RR block in your PyTorch model:

```python
import torch
import torch.nn as nn
from rr_block import RR

class SimpleModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(SimpleModel, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.rr = RR(128, [nn.ReLU(), nn.Sigmoid()])
        self.fc2 = nn.Linear(128, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.rr(x)
        x = self.fc2(x)
        return x

```

## Build and Development

To build the package from source, you can use the following commands:

```bash
pip install -e .
```
This will install the package in editable mode, allowing you to make changes to the source code and have them reflected in your Python environment.
