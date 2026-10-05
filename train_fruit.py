import tensorflow as tf
from tensorflow.keras import layers, models
import os

# ==============================
# SETTINGS
# ==============================

image_size = (128, 128)
batch_size = 16
epochs = 20

dataset_path = "dataset/fruit"


# ==============================
# LOAD DATASET
# ==============================

train_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=image_size,
    batch_size=batch_size,
    color_mode="grayscale"
)

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=image_size,
    batch_size=batch_size,
    color_mode="grayscale"
)


# ==============================
# CLASS NAMES
# ==============================

class_names = train_dataset.class_names

print("================================")
print("       FRUIT CLASSES")
print("================================")
print(class_names)


# ==============================
# DATA AUGMENTATION
# ==============================

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1)
])


# ==============================
# SHAPE-FOCUSED CNN MODEL
# ==============================

model = models.Sequential([

    layers.Input(shape=(128, 128, 1)),

    data_augmentation,

    # Normalize grayscale image
    layers.Rescaling(1./255),

    # First feature extraction
    layers.Conv2D(
        32,
        (3, 3),
        activation="relu"
    ),
    layers.MaxPooling2D(),

    # Second feature extraction
    layers.Conv2D(
        64,
        (3, 3),
        activation="relu"
    ),
    layers.MaxPooling2D(),

    # Third feature extraction
    layers.Conv2D(
        128,
        (3, 3),
        activation="relu"
    ),
    layers.MaxPooling2D(),

    layers.Dropout(0.3),

    layers.Flatten(),

    layers.Dense(
        128,
        activation="relu"
    ),

    layers.Dropout(0.5),

    # Fruit classes
    layers.Dense(
        len(class_names),
        activation="softmax"
    )
])


# ==============================
# COMPILE MODEL
# ==============================

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


# ==============================
# MODEL SUMMARY
# ==============================

model.summary()


# ==============================
# TRAIN
# ==============================

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=epochs
)


# ==============================
# SAVE MODEL
# ==============================

os.makedirs("models", exist_ok=True)

model.save(
    "models/fruit_classifier.keras"
)

print("================================")
print(" Shape-Based Fruit Model Saved!")
print("================================")