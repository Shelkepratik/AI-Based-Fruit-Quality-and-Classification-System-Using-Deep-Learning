import os
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt


# ==========================================
# 1. Dataset Path
# ==========================================

dataset_path = "dataset/quality"

img_size = (128, 128)
batch_size = 32


# ==========================================
# 2. Load Training Dataset
# ==========================================

train_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=img_size,
    batch_size=batch_size
)


# ==========================================
# 3. Load Validation Dataset
# ==========================================

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=img_size,
    batch_size=batch_size
)


# ==========================================
# 4. Get Class Names
# ==========================================

class_names = train_dataset.class_names

print("Quality Classes:")
print(class_names)


# ==========================================
# 5. Improve Performance
# ==========================================

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(
    buffer_size=AUTOTUNE
)

validation_dataset = validation_dataset.prefetch(
    buffer_size=AUTOTUNE
)


# ==========================================
# 6. Create CNN Model
# ==========================================

model = models.Sequential([

    layers.Input(shape=(128, 128, 3)),

    # Normalize pixel values
    layers.Rescaling(1.0 / 255),

    # CNN Layer 1
    layers.Conv2D(
        32,
        (3, 3),
        activation="relu"
    ),

    layers.MaxPooling2D(),

    # CNN Layer 2
    layers.Conv2D(
        64,
        (3, 3),
        activation="relu"
    ),

    layers.MaxPooling2D(),

    # CNN Layer 3
    layers.Conv2D(
        128,
        (3, 3),
        activation="relu"
    ),

    layers.MaxPooling2D(),

    # Flatten
    layers.Flatten(),

    # Fully Connected Layer
    layers.Dense(
        128,
        activation="relu"
    ),

    # Prevent overfitting
    layers.Dropout(0.5),

    # Output Layer
    layers.Dense(
        len(class_names),
        activation="softmax"
    )
])


# ==========================================
# 7. Compile Model
# ==========================================

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


# ==========================================
# 8. Display Model
# ==========================================

model.summary()


# ==========================================
# 9. Train Model
# ==========================================

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=15
)


# ==========================================
# 10. Create Models Folder
# ==========================================

os.makedirs(
    "models",
    exist_ok=True
)


# ==========================================
# 11. Save Model
# ==========================================

model.save(
    "models/quality_classifier.keras"
)

print(
    "Quality classification model saved successfully!"
)


# ==========================================
# 12. Plot Accuracy
# ==========================================

plt.plot(
    history.history["accuracy"],
    label="Training Accuracy"
)

plt.plot(
    history.history["val_accuracy"],
    label="Validation Accuracy"
)

plt.xlabel("Epoch")
plt.ylabel("Accuracy")

plt.title(
    "Fruit Quality Classification Accuracy"
)

plt.legend()

plt.show()


# ==========================================
# 13. Plot Loss
# ==========================================

plt.plot(
    history.history["loss"],
    label="Training Loss"
)

plt.plot(
    history.history["val_loss"],
    label="Validation Loss"
)

plt.xlabel("Epoch")
plt.ylabel("Loss")

plt.title(
    "Fruit Quality Classification Loss"
)

plt.legend()

plt.show()