import tensorflow as tf
from tensorflow.keras import layers
import os


# ==============================
# SETTINGS
# ==============================

image_size = (160, 160)
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
    seed=42,
    image_size=image_size,
    batch_size=batch_size
)

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=image_size,
    batch_size=batch_size
)


# ==============================
# CLASS NAMES
# ==============================

class_names = train_dataset.class_names

print("\nFruit Classes:")
print(class_names)


# ==============================
# PERFORMANCE
# ==============================

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(
    buffer_size=AUTOTUNE
)

validation_dataset = validation_dataset.prefetch(
    buffer_size=AUTOTUNE
)


# ==============================
# DATA AUGMENTATION
# ==============================

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1)
])


# ==============================
# MOBILE NET V2
# ==============================

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(160, 160, 3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False


# ==============================
# MODEL
# ==============================

inputs = tf.keras.Input(
    shape=(160, 160, 3)
)

x = data_augmentation(inputs)

x = tf.keras.applications.mobilenet_v2.preprocess_input(x)

x = base_model(x, training=False)

x = layers.GlobalAveragePooling2D()(x)

x = layers.Dropout(0.3)(x)

outputs = layers.Dense(
    len(class_names),
    activation="softmax"
)(x)

model = tf.keras.Model(
    inputs,
    outputs
)


# ==============================
# COMPILE
# ==============================

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


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

os.makedirs(
    "models",
    exist_ok=True
)

model.save(
    "models/mobile_fruit_unknown_classifier.keras"
)

print("\n================================")
print("5-CLASS MODEL TRAINING COMPLETE")
print("================================")

print("Classes:")
print(class_names)

print("\nModel saved:")
print("models/mobile_fruit_unknown_classifier.keras")