import tensorflow as tf
import numpy as np
from PIL import Image

# ============================================
# LOAD MODEL
# ============================================

model = tf.keras.models.load_model(
    "models/mobile_fruit_classifier.keras"
)

# ============================================
# CLASS NAMES
# ============================================

fruit_classes = [
    "apple",
    "banana",
    "mango",
    "orange"
]

# ============================================
# IMAGE PATH
# ============================================

image_path = input(
    "Enter fruit image path: "
).strip().strip('"')

# ============================================
# LOAD IMAGE
# ============================================

image = Image.open(
    image_path
).convert("RGB"
)

print("Image loaded successfully!")

# ============================================
# RESIZE
# ============================================

image = image.resize(
    (160, 160)
)

# ============================================
# CONVERT TO ARRAY
# ============================================

image_array = np.array(
    image
).astype("float32")

image_array = np.expand_dims(
    image_array,
    axis=0
)

# ============================================
# MOBILE NET PREDICTION
# ============================================

prediction = model.predict(
    image_array,
    verbose=0
)

fruit_index = np.argmax(
    prediction[0]
)

fruit = fruit_classes[
    fruit_index
]

confidence = (
    prediction[0][fruit_index] * 100
)

# ============================================
# RESULT
# ============================================

print()
print("==============================")
print("   MOBILE FRUIT PREDICTION")
print("==============================")

print(
    "Fruit      :",
    fruit
)

print(
    "Confidence :",
    round(float(confidence), 2),
    "%"
)

print("==============================")