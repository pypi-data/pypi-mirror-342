
# damage_layers

This package provides a custom Keras layer `JointDamageDense` which introduces learnable neuron-level "damage" scalars `d` alongside weights `W`. It is designed for exploring neuron fatigue, sparsity, or structural regularisation in neural networks.

## Installation

```
pip install .
```

## Usage

```python
from damage_layers import JointDamageDense

model = tf.keras.Sequential([
    JointDamageDense(16, activation='relu', input_shape=(2,)),
    JointDamageDense(16, activation='relu'),
    JointDamageDense(1, activation='linear')
])
```
