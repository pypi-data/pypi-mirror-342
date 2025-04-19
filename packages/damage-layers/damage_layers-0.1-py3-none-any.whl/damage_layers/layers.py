
import tensorflow as tf

class JointDamageDense(tf.keras.layers.Layer):
    def __init__(self, units, activation=None, **kwargs):
        super().__init__(**kwargs)
        self.units = units
        self.activation = tf.keras.activations.get(activation)

    def build(self, input_shape):
        self.w = self.add_weight(
            shape=(input_shape[-1], self.units),
            initializer='glorot_uniform',
            trainable=True,
            name="weights"
        )
        self.b = self.add_weight(
            shape=(self.units,),
            initializer='zeros',
            trainable=True,
            name="bias"
        )
        self.d = self.add_weight(
            shape=(self.units,),
            initializer=tf.keras.initializers.RandomUniform(0.7, 1.0),
            trainable=True,
            name="damage"
        )

    def call(self, inputs):
        z = tf.matmul(inputs, self.w) + self.b
        a = self.activation(z)
        return a * self.d
