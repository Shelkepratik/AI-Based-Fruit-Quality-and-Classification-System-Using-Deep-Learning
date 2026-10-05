import tensorflow as tf
from tensorflow.keras import layers, models
import os

# ============================================
# SETTINGS
# ============================================

image_size = (160, 160)
batch_size = 16
epochs = 15

dataset_path = "dataset/fruit"

# ============================================
# LOAD TRAINING DATA
# ============================================

train_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=image_size,
    batch_size=batch_size
)

# ============================================
# LOAD VALIDATION DATA
# ============================================

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=image_size,
    batch_size=batch_size
)

# ============================================
# CLASS NAMES
# ============================================

class_names = train_dataset.class_names

print()
print("================================")
print("       FRUIT CLASSES")
print("================================")
print(class_names)

# ============================================
# DATA AUGMENTATION
# ============================================

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
    layers.RandomContrast(0.1)
])

# ============================================
# LOAD MOBILENETV2
# ============================================

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(160, 160, 3),
    include_top=False,
    weights="imagenet"
)

# Freeze MobileNetV2
base_model.trainable = False

# ============================================
# CREATE MODEL
# ============================================

inputs = layers.Input(
    shape=(160, 160, 3)
)

x = data_augmentation(inputs)

# MobileNetV2 preprocessing
x = tf.keras.applications.mobilenet_v2.preprocess_input(x)

x = base_model(
    x,
    training=False
)

x = layers.GlobalAveragePooling2D()(x)

x = layers.Dropout(0.3)(x)

x = layers.Dense(
    128,
    activation="relu"
)(x)

x = layers.Dropout(0.3)(x)

outputs = layers.Dense(
    len(class_names),
    activation="softmax"
)(x)

model = models.Model(
    inputs,
    outputs
)

# ============================================
# COMPILE MODEL
# ============================================

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# ============================================
# MODEL SUMMARY
# ============================================

model.summary()

# ============================================
# TRAIN MODEL
# ============================================

print()
print("================================")
print("       TRAINING STARTED")
print("================================")

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=epochs
)

# ============================================
# SAVE MODEL
# ============================================

os.makedirs(
    "models",
    exist_ok=True
)

model.save(
    "models/mobile_fruit_classifier.keras"
)

# ============================================
# FINAL RESULTS
# ============================================

print()
print("================================")
print("       TRAINING COMPLETE")
print("================================")

print(
    "Final Training Accuracy :",
    round(
        history.history["accuracy"][-1] * 100,
        2
    ),
    "%"
)

print(
    "Final Validation Accuracy :",
    round(
        history.history["val_accuracy"][-1] * 100,
        2
    ),
    "%"
)

print()
print("Model saved successfully:")
print(
    "models/mobile_fruit_classifier.keras"
)

print("================================")