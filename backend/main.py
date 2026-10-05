import tensorflow as tf
import numpy as np
import cv2

from PIL import Image
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO


app = FastAPI()


# ==============================
# CORS
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==============================
# LOAD MODELS
# ==============================

fruit_model = tf.keras.models.load_model(
    "../models/fruit_classifier.keras"
)

quality_model = tf.keras.models.load_model(
    "../models/quality_classifier.keras"
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
# HOME API
# ==============================

@app.get("/")
def home():

    return {
        "message": "Fruit Quality Analyzer API is running!"
    }


# ==============================
# PREDICTION API
# ==============================

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # ==============================
    # READ UPLOADED IMAGE
    # ==============================

    image_data = await file.read()

    image = Image.open(
        BytesIO(image_data)
    ).convert("RGB")


    # Convert PIL image to NumPy
    image_array = np.array(image)


    # ==================================================
    # SHAPE PROCESSING FOR FRUIT CLASSIFICATION
    # ==================================================

    # Convert RGB image to grayscale
    gray_image = cv2.cvtColor(
        image_array,
        cv2.COLOR_RGB2GRAY
    )


    # Detect edges
    shape_image = cv2.Canny(
        gray_image,
        100,
        200
    )


    # Resize to model input size
    shape_image = cv2.resize(
        shape_image,
        (128, 128)
    )


    # Add channel dimension
    # (128,128) → (128,128,1)
    shape_image = np.expand_dims(
        shape_image,
        axis=-1
    )


    # Add batch dimension
    # (128,128,1) → (1,128,128,1)
    shape_image = np.expand_dims(
        shape_image,
        axis=0
    )


    # ==================================================
    # RGB PROCESSING FOR QUALITY CLASSIFICATION
    # ==================================================

    rgb_image = cv2.resize(
        image_array,
        (128, 128)
    )


    # Add batch dimension
    # (128,128,3) → (1,128,128,3)
    rgb_image = np.expand_dims(
        rgb_image,
        axis=0
    )


    # ==============================
    # FRUIT PREDICTION
    # ==============================

    fruit_prediction = fruit_model.predict(
        shape_image,
        verbose=0
    )


    fruit_index = np.argmax(
        fruit_prediction[0]
    )


    fruit = fruit_classes[
        fruit_index
    ]


    fruit_confidence = float(
        fruit_prediction[0][fruit_index] * 100
    )


    # ==============================
    # QUALITY PREDICTION
    # ==============================

    quality_prediction = quality_model.predict(
        rgb_image,
        verbose=0
    )


    quality_index = np.argmax(
        quality_prediction[0]
    )


    quality = quality_classes[
        quality_index
    ]


    quality_confidence = float(
        quality_prediction[0][quality_index] * 100
    )


    # ==============================
    # GET FRUIT INFORMATION
    # ==============================

    info = fruit_info[
        fruit
    ]


    # ==============================
    # RETURN RESULT
    # ==============================

    return {

        "fruit": info["name"],

        "fruit_confidence": round(
            fruit_confidence,
            2
        ),

        "quality": quality,

        "quality_confidence": round(
            quality_confidence,
            2
        ),

        "calories": info["calories"],

        "fiber": info["fiber"],

        "vitamins": info["vitamins"],

        "reference_price": info["reference_price"]
    }