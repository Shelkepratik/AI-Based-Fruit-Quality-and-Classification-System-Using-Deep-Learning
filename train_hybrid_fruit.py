import tensorflow as tf
from tensorflow.keras import layers, Model
import numpy as np
import os

# ==============================
# SETTINGS
# ==============================

image_size = (128, 128)
batch_size = 16
epochs = 20

dataset_path = "dataset/fruit"

classes = [
    "apple",
    "banana",
    "mango",
    "orange"
]

extensions = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
)


# ==============================
# FIND IMAGE FILES
# ==============================

file_paths = []
labels = []

for label, fruit in enumerate(classes):

    folder = os.path.join(
        dataset_path,
        fruit
    )

    for file in os.listdir(folder):

        if file.lower().endswith(extensions):

            file_paths.append(
                os.path.join(folder, file)
            )

            labels.append(label)


file_paths = np.array(file_paths)
labels = np.array(labels)


# ==============================
# SHUFFLE DATA
# ==============================

rng = np.random.default_rng(123)

indices = np.arange(
    len(file_paths)
)

rng.shuffle(indices)

file_paths = file_paths[indices]
labels = labels[indices]


# ==============================
# TRAIN / VALIDATION SPLIT
# ==============================

split_index = int(
    len(file_paths) * 0.8
)

train_paths = file_paths[
    :split_index
]

train_labels = labels[
    :split_index
]

validation_paths = file_paths[
    split_index:
]

validation_labels = labels[
    split_index:
]


# ==============================
# DATASET INFORMATION
# ==============================

print("================================")
print("      HYBRID FRUIT DATASET")
print("================================")

print(
    f"Total images      : {len(file_paths)}"
)

print(
    f"Training images   : {len(train_paths)}"
)

print(
    f"Validation images : {len(validation_paths)}"
)

print(
    f"Classes           : {classes}"
)

print("================================")


# ==============================
# IMAGE PROCESSING
# ==============================

def load_image(path, label):

    # Read image
    image = tf.io.read_file(path)

    # Decode image
    image = tf.image.decode_image(
        image,
        channels=3,
        expand_animations=False
    )

    # Resize
    image = tf.image.resize(
        image,
        image_size
    )

    # Convert to float
    image = tf.cast(
        image,
        tf.float32
    )

    # ==========================
    # RGB IMAGE
    # ==========================

    rgb_image = image / 255.0

    # ==========================
    # SHAPE / EDGE IMAGE
    # ==========================

    gray = tf.image.rgb_to_grayscale(
        image
    )

    # Horizontal difference
    dx = (
        gray[:, 1:, :]
        -
        gray[:, :-1, :]
    )

    # Vertical difference
    dy = (
        gray[1:, :, :]
        -
        gray[:-1, :, :]
    )

    # Padding
    dx = tf.pad(
        dx,
        [
            [0, 0],
            [0, 1],
            [0, 0]
        ]
    )

    dy = tf.pad(
        dy,
        [
            [0, 1],
            [0, 0],
            [0, 0]
        ]
    )

    # Edge strength
    edges = tf.sqrt(
        tf.square(dx)
        +
        tf.square(dy)
    )

    # Normalize edges
    edges = edges / (
        tf.reduce_max(edges)
        +
        1e-7
    )

    return {
        "rgb_input": rgb_image,
        "shape_input": edges
    }, label


# ==============================
# TRAIN DATASET
# ==============================

train_dataset = (
    tf.data.Dataset
    .from_tensor_slices(
        (
            train_paths,
            train_labels
        )
    )
)

train_dataset = train_dataset.shuffle(
    buffer_size=len(train_paths),
    seed=123
)

train_dataset = train_dataset.map(
    load_image,
    num_parallel_calls=tf.data.AUTOTUNE
)

train_dataset = train_dataset.batch(
    batch_size
)

train_dataset = train_dataset.prefetch(
    tf.data.AUTOTUNE
)


# ==============================
# VALIDATION DATASET
# ==============================

validation_dataset = (
    tf.data.Dataset
    .from_tensor_slices(
        (
            validation_paths,
            validation_labels
        )
    )
)

validation_dataset = validation_dataset.map(
    load_image,
    num_parallel_calls=tf.data.AUTOTUNE
)

validation_dataset = validation_dataset.batch(
    batch_size
)

validation_dataset = validation_dataset.prefetch(
    tf.data.AUTOTUNE
)


# ==============================
# RGB CNN BRANCH
# ==============================

rgb_input = layers.Input(
    shape=(128, 128, 3),
    name="rgb_input"
)

rgb = layers.Conv2D(
    32,
    (3, 3),
    activation="relu"
)(rgb_input)

rgb = layers.MaxPooling2D()(rgb)

rgb = layers.Conv2D(
    64,
    (3, 3),
    activation="relu"
)(rgb)

rgb = layers.MaxPooling2D()(rgb)

rgb = layers.Conv2D(
    128,
    (3, 3),
    activation="relu"
)(rgb)

rgb = layers.MaxPooling2D()(rgb)

rgb = layers.GlobalAveragePooling2D()(rgb)


# ==============================
# SHAPE CNN BRANCH
# ==============================

shape_input = layers.Input(
    shape=(128, 128, 1),
    name="shape_input"
)

shape = layers.Conv2D(
    32,
    (3, 3),
    activation="relu"
)(shape_input)

shape = layers.MaxPooling2D()(shape)

shape = layers.Conv2D(
    64,
    (3, 3),
    activation="relu"
)(shape)

shape = layers.MaxPooling2D()(shape)

shape = layers.Conv2D(
    128,
    (3, 3),
    activation="relu"
)(shape)

shape = layers.MaxPooling2D()(shape)

shape = layers.GlobalAveragePooling2D()(shape)


# ==============================
# COMBINE FEATURES
# ==============================

combined = layers.Concatenate()(
    [
        rgb,
        shape
    ]
)

combined = layers.Dense(
    128,
    activation="relu"
)(combined)

combined = layers.Dropout(
    0.5
)(combined)


# ==============================
# OUTPUT
# ==============================

output = layers.Dense(
    len(classes),
    activation="softmax",
    name="fruit_output"
)(combined)


# ==============================
# CREATE MODEL
# ==============================

model = Model(
    inputs=[
        rgb_input,
        shape_input
    ],
    outputs=output
)


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
# TRAIN MODEL
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
    "models/hybrid_fruit_classifier.keras"
)


# ==============================
# COMPLETION MESSAGE
# ==============================

print("================================")
print(" Hybrid Fruit Model Saved!")
print("================================")

print(
    "models/hybrid_fruit_classifier.keras"
)

print("================================")