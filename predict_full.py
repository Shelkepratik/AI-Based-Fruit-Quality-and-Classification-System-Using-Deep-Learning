import tensorflow as tf
import numpy as np
from PIL import Image

# ==============================
# FRUIT INFORMATION
# ==============================

fruit_info = {

    "apple": {
        "name": "Apple",
        "calories": "52 kcal",
        "fiber": "2.4 g",
        "vitamins": "Vitamin C, Vitamin K",
        "reference_price": "₹120 per kg"
    },

    "banana": {
        "name": "Banana",
        "calories": "89 kcal",
        "fiber": "2.6 g",
        "vitamins": "Vitamin B6, Vitamin C",
        "reference_price": "₹60 per kg"
    },

    "mango": {
        "name": "Mango",
        "calories": "60 kcal",
        "fiber": "1.6 g",
        "vitamins": "Vitamin A, Vitamin C",
        "reference_price": "₹100 per kg"
    },

    "orange": {
        "name": "Orange",
        "calories": "47 kcal",
        "fiber": "2.4 g",
        "vitamins": "Vitamin C, Folate",
        "reference_price": "₹80 per kg"
    }
}


# ==============================
# LOAD MODELS
# ==============================

fruit_model = tf.keras.models.load_model(
    "models/fruit_classifier.keras"
)

quality_model = tf.keras.models.load_model(
    "models/quality_classifier.keras"
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

quality_classes = [
    "Poor",
    "average",
    "good"
]


# ==============================
# GET IMAGE PATH
# ==============================

image_path = input(
    "Enter fruit image path: "
).strip().strip('"')


# ==============================
# LOAD IMAGE
# ==============================

image = Image.open(image_path)

print("\nImage loaded successfully!")


# ==============================
# PREPARE IMAGE
# ==============================

image = image.resize((128, 128))

image_array = np.array(image)

image_array = np.expand_dims(
    image_array,
    axis=0
)


# ==============================
# FRUIT PREDICTION
# ==============================

fruit_prediction = fruit_model.predict(
    image_array,
    verbose=0
)

fruit_index = np.argmax(
    fruit_prediction[0]
)

fruit = fruit_classes[fruit_index]

fruit_confidence = (
    fruit_prediction[0][fruit_index] * 100
)


# ==============================
# QUALITY PREDICTION
# ==============================

quality_prediction = quality_model.predict(
    image_array,
    verbose=0
)

quality_index = np.argmax(
    quality_prediction[0]
)

quality = quality_classes[quality_index]

quality_confidence = (
    quality_prediction[0][quality_index] * 100
)


# ==============================
# GET FRUIT INFORMATION
# ==============================

info = fruit_info[fruit]


# ==============================
# DISPLAY FINAL RESULT
# ==============================

print()
print("======================================")
print("       FRUIT QUALITY ANALYZER")
print("======================================")

print("Fruit           :", info["name"])
print("Fruit Confidence:", round(fruit_confidence, 2), "%")

print("--------------------------------------")

print("Quality         :", quality)
print("Quality Confidence:", round(quality_confidence, 2), "%")

print("--------------------------------------")

print("Calories        :", info["calories"])
print("Fiber           :", info["fiber"])
print("Vitamins        :", info["vitamins"])
print("Reference Price:", info["reference_price"])

print("======================================")