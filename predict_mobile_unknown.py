import tensorflow as tf
import numpy as np
from PIL import Image


# Load 5-class model
model = tf.keras.models.load_model(
    "models/mobile_fruit_unknown_classifier.keras"
)


# Class names
class_names = [
    "apple",
    "banana",
    "mango",
    "orange",
    "unknown"
]


# Ask for image
image_path = input(
    "Enter image path: "
).strip().strip('"')


# Open image
image = Image.open(
    image_path
).convert("RGB")


# Resize
image = image.resize(
    (160, 160)
)


# Convert to NumPy
image_array = np.array(
    image
)


# Add batch dimension
image_array = np.expand_dims(
    image_array,
    axis=0
)


# Predict
prediction = model.predict(
    image_array,
    verbose=0
)


# Get predicted class
index = int(
    np.argmax(
        prediction[0]
    )
)

fruit = class_names[index]

confidence = float(
    prediction[0][index] * 100
)


# Display result
print("\n==============================")
print("5-CLASS FRUIT PREDICTION")
print("==============================")

print("Fruit      :", fruit)
print("Confidence :", round(confidence, 2), "%")