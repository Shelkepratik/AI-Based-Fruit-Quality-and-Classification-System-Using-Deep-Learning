import tensorflow as tf
import numpy as np
from PIL import Image

# ==============================
# LOAD HYBRID MODEL
# ==============================

model = tf.keras.models.load_model(
    "models/hybrid_fruit_classifier.keras"
)

# ==============================
# CLASS NAMES
# ==============================

fruit_classes = [
    "apple",
    "banana",
    "mango",
    "orange"
]

# ==============================
# IMAGE PATH
# ==============================

image_path = input(
    "Enter fruit image path: "
).strip().strip('"')

# ==============================
# LOAD IMAGE
# ==============================

image = Image.open(
    image_path
).convert("RGB")

print("Image loaded successfully!")

# Resize
image = image.resize(
    (128, 128)
)

# Convert to NumPy
image_array = np.array(
    image
).astype("float32")

# ==============================
# RGB INPUT
# ==============================

rgb_image = image_array / 255.0

rgb_image = np.expand_dims(
    rgb_image,
    axis=0
)

# ==============================
# SHAPE INPUT
# ==============================

gray = tf.image.rgb_to_grayscale(
    image_array
)

dx = (
    gray[:, 1:, :]
    -
    gray[:, :-1, :]
)

dy = (
    gray[1:, :, :]
    -
    gray[:-1, :, :]
)

dx = tf.pad(
    dx,
    [
        [0, 0],
        [0, 1],
        [0, 0]
    ]
)

dy = tf.pad(
    dy,
    [
        [0, 1],
        [0, 0],
        [0, 0]
    ]
)

edges = tf.sqrt(
    tf.square(dx)
    +
    tf.square(dy)
)

edges = edges / (
    tf.reduce_max(edges)
    + 1e-7
)

shape_image = np.expand_dims(
    edges.numpy(),
    axis=0
)

# ==============================
# PREDICTION
# ==============================

prediction = model.predict(
    {
        "rgb_input": rgb_image,
        "shape_input": shape_image
    },
    verbose=0
)

index = np.argmax(
    prediction[0]
)

fruit = fruit_classes[index]

confidence = (
    prediction[0][index] * 100
)

# ==============================
# RESULT
# ==============================

print()
print("==============================")
print("   HYBRID FRUIT PREDICTION")
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