# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense

# Training data for XOR
X = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
y = np.array([[0], [1], [1], [0]])

# Build the model
model = Sequential([
    Input(shape=(2,)),   
    Dense(3, activation='sigmoid'),  # Hidden layer with 3 neurons
    Dense(1, activation='sigmoid')   # Output layer
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=10000, verbose=0)  # verbose=0 suppresses output for simplicity

# Test the model
predictions = model.predict(X)
print("Predictions:")
print(predictions)