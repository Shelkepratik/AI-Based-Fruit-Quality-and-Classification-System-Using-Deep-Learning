import tensorflow as tf
import numpy as np
from PIL import Image


# ==========================================
# 1. Load Trained Model
# ==========================================

model = tf.keras.models.load_model(
    "models/fruit_classifier.keras"
)


# ==========================================
# 2. Fruit Class Names
# ==========================================

class_names = [
    "apple",
    "banana",
    "mango",
    "orange"
]


# ==========================================
# 3. Get Image Path
# ==========================================

image_path = input("Enter fruit image path: ")


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
# 6. Convert Image to NumPy Array
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
# 8. Make Prediction
# ==========================================

prediction = model.predict(image_array)


# ==========================================
# 9. Find Highest Probability
# ==========================================

predicted_index = np.argmax(prediction[0])

predicted_fruit = class_names[predicted_index]

confidence = prediction[0][predicted_index] * 100


# ==========================================
# 10. Display Result
# ==========================================

print()
print("==============================")
print("     FRUIT PREDICTION")
print("==============================")

print("Fruit      :", predicted_fruit)
print("Confidence :", round(confidence, 2), "%")

print("==============================")