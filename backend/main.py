import tensorflow as tf
import numpy as np

from PIL import Image
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO


# ==================================================
# CREATE FASTAPI APP
# ==================================================

app = FastAPI(
    title="Fruit Quality Analyzer API",
    description="AI-based Fruit Classification and Visual Quality Assessment",
    version="1.0"
)


# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==================================================
# LOAD FRUIT MODEL
# ==================================================

fruit_model = tf.keras.models.load_model(
    "../models/mobile_fruit_unknown_classifier.keras"
)


# ==================================================
# LOAD QUALITY MODEL
# ==================================================

quality_model = tf.keras.models.load_model(
    "../models/quality_classifier.keras"
)


# ==================================================
# CLASS NAMES
# ==================================================

fruit_classes = [
    "apple",
    "banana",
    "mango",
    "orange",
    "unknown"
]

quality_classes = [
    "Poor",
    "average",
    "good"
]


# ==================================================
# FRUIT INFORMATION
# ==================================================

fruit_info = {

    "apple": {
        "name": "Apple",
        "calories": "52 kcal",
        "fiber": "2.4 g",
        "vitamins": "Vitamin C, Vitamin K",
        "reference_price": 120
    },

    "banana": {
        "name": "Banana",
        "calories": "89 kcal",
        "fiber": "2.6 g",
        "vitamins": "Vitamin B6, Vitamin C",
        "reference_price": 60
    },

    "mango": {
        "name": "Mango",
        "calories": "60 kcal",
        "fiber": "1.6 g",
        "vitamins": "Vitamin A, Vitamin C",
        "reference_price": 100
    },

    "orange": {
        "name": "Orange",
        "calories": "47 kcal",
        "fiber": "2.4 g",
        "vitamins": "Vitamin C, Folate",
        "reference_price": 80
    }
}


# ==================================================
# HOME API
# ==================================================

@app.get("/")
def home():

    return {
        "message": "Fruit Quality Analyzer API is running!",
        "fruit_model": "MobileNetV2 - 5 Classes",
        "fruit_classes": fruit_classes,
        "fruit_input_size": "160x160 RGB",
        "quality_input_size": "128x128 RGB"
    }


# ==================================================
# PREDICTION API
# ==================================================

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):

    # ==================================================
    # READ IMAGE
    # ==================================================

    image_data = await file.read()

    image = Image.open(
        BytesIO(image_data)
    ).convert("RGB")


    # ==================================================
    # FRUIT CLASSIFICATION
    # ==================================================

    fruit_image = image.resize(
        (160, 160)
    )

    fruit_image_array = np.array(
        fruit_image
    )

    fruit_image_array = np.expand_dims(
        fruit_image_array,
        axis=0
    )


    # ==================================================
    # FRUIT PREDICTION
    # ==================================================

    fruit_prediction = fruit_model.predict(
        fruit_image_array,
        verbose=0
    )


    fruit_index = int(
        np.argmax(
            fruit_prediction[0]
        )
    )


    fruit = fruit_classes[
        fruit_index
    ]


    fruit_confidence = float(
        fruit_prediction[0][fruit_index] * 100
    )


    # ==================================================
    # UNKNOWN FRUIT CHECK
    # ==================================================

    if fruit == "unknown":

        return {

            "fruit": "Unknown Fruit",

            "fruit_confidence": round(
                fruit_confidence,
                2
            ),

            "quality": "Not Available",

            "quality_confidence": 0,

            "calories": "Not Available",

            "fiber": "Not Available",

            "vitamins": "Not Available",

            "reference_price": "Not Available",

            "message": "The uploaded image does not appear to be one of the supported fruits."
        }


    # ==================================================
    # QUALITY CLASSIFICATION
    # ==================================================

    quality_image = image.resize(
        (128, 128)
    )

    quality_image_array = np.array(
        quality_image
    )

    quality_image_array = np.expand_dims(
        quality_image_array,
        axis=0
    )


    # ==================================================
    # QUALITY PREDICTION
    # ==================================================

    quality_prediction = quality_model.predict(
        quality_image_array,
        verbose=0
    )


    quality_index = int(
        np.argmax(
            quality_prediction[0]
        )
    )


    quality = quality_classes[
        quality_index
    ]


    quality_confidence = float(
        quality_prediction[0][quality_index] * 100
    )


    # ==================================================
    # GET FRUIT INFORMATION
    # ==================================================

    info = fruit_info[
        fruit
    ]


    # ==================================================
    # QUALITY BASED PRICE
    # ==================================================

    base_price = info["reference_price"]


    if quality.lower() == "good":

        final_price = base_price

    elif quality.lower() == "average":

        final_price = base_price * 0.70

    else:

        final_price = 0


    # ==================================================
    # FORMAT PRICE
    # ==================================================

    final_price = f"₹{final_price:.0f} per kg"


    # ==================================================
    # RETURN RESULT
    # ==================================================

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

        "reference_price": final_price
    }