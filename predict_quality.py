import tensorflow as tf
import numpy as np
from PIL import Image


# ==========================================
# 1. Load Quality Model
# ==========================================

model = tf.keras.models.load_model(
    "models/quality_classifier.keras"
)


# ==========================================
# 2. Quality Class Names
# ==========================================

class_names = [
    "Poor",
    "average",
    "good"
]


# ==========================================
# 3. Get Image Path
# ==========================================

image_path = input(
    "Enter fruit image path: "
).strip().strip('"')


# ==========================================
# 4. Load Image
# ==========================================

image = Image.open(image_path)

print("Image loaded successfully!")


# ==========================================
# 5. Resize Image
# ==========================================

image = image.resize((128, 128))


# ==========================================
# 6. Convert to NumPy Array
# ==========================================

image_array = np.array(image)


# ==========================================
# 7. Add Batch Dimension
# ==========================================

image_array = np.expand_dims(
    image_array,
    axis=0
)


# ==========================================
# 8. Prediction
# ==========================================

prediction = model.predict(image_array)


# ==========================================
# 9. Find Predicted Class
# ==========================================

predicted_index = np.argmax(
    prediction[0]
)

predicted_quality = class_names[
    predicted_index
]

confidence = (
    prediction[0][predicted_index] * 100
)


# ==========================================
# 10. Display Result
# ==========================================

print()
print("==============================")
print("      QUALITY PREDICTION")
print("==============================")

print(
    "Quality    :",
    predicted_quality
)

print(
    "Confidence :",
    round(confidence, 2),
    "%"
)

print("==============================")