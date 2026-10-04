import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import os

# ==============================
# 1. Load Dataset
# ==============================

dataset_path = "dataset/fruit"

img_size = (128, 128)
batch_size = 32


train_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=img_size,
    batch_size=batch_size
)


validation_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=img_size,
    batch_size=batch_size
)


# ==============================
# 2. Check Fruit Classes
# ==============================

class_names = train_dataset.class_names

print("Fruit Classes:")
print(class_names)


# ==============================
# 3. Improve Dataset Performance
# ==============================

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(
    buffer_size=AUTOTUNE
)

validation_dataset = validation_dataset.prefetch(
    buffer_size=AUTOTUNE
)


# ==============================
# 4. Create CNN Model
# ==============================

model = models.Sequential([

    # Input + Normalization
    layers.Rescaling(1.0 / 255, input_shape=(128, 128, 3)),

    # First CNN layer
    layers.Conv2D(32, (3, 3), activation="relu"),
    layers.MaxPooling2D(),

    # Second CNN layer
    layers.Conv2D(64, (3, 3), activation="relu"),
    layers.MaxPooling2D(),

    # Third CNN layer
    layers.Conv2D(128, (3, 3), activation="relu"),
    layers.MaxPooling2D(),

    # Convert feature maps into one dimension
    layers.Flatten(),

    # Fully connected layer
    layers.Dense(128, activation="relu"),

    # Prevent overfitting
    layers.Dropout(0.5),

    # Output layer
    layers.Dense(len(class_names), activation="softmax")
])


# ==============================
# 5. Compile Model
# ==============================

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


# ==============================
# 6. Display Model Structure
# ==============================

model.summary()


# ==============================
# 7. Train CNN
# ==============================

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=15
)


# ==============================
# 8. Save Model
# ==============================
os.makedirs("models", exist_ok=True)
model.save("models/fruit_classifier.keras")

print("Fruit classification model saved successfully!")


# ==============================
# 9. Plot Accuracy
# ==============================

plt.plot(history.history["accuracy"], label="Training Accuracy")
plt.plot(history.history["val_accuracy"], label="Validation Accuracy")

plt.xlabel("Epoch")
plt.ylabel("Accuracy")

plt.title("Fruit Classification Accuracy")

plt.legend()

plt.show()


# ==============================
# 10. Plot Loss
# ==============================

plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")

plt.xlabel("Epoch")
plt.ylabel("Loss")

plt.title("Fruit Classification Loss")

plt.legend()

plt.show()