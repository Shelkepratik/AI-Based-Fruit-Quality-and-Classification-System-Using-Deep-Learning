import cv2
import os

# Original dataset
input_folder = "dataset/fruit"

# Shape dataset
output_folder = "dataset/shape"

classes = [
    "apple",
    "banana",
    "mango",
    "orange"
]

extensions = (".jpg", ".jpeg", ".png", ".webp")


for fruit in classes:

    input_path = os.path.join(input_folder, fruit)
    output_path = os.path.join(output_folder, fruit)

    os.makedirs(output_path, exist_ok=True)

    count = 0

    for file in os.listdir(input_path):

        if file.lower().endswith(extensions):

            image_path = os.path.join(input_path, file)

            # Read image
            image = cv2.imread(image_path)

            if image is None:
                continue

            # Convert to grayscale
            gray = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2GRAY
            )

            # Detect edges
            edges = cv2.Canny(
                gray,
                100,
                200
            )

            # Save shape image
            output_path_file = os.path.join(
                output_path,
                file
            )

            cv2.imwrite(
                output_path_file,
                edges
            )

            count += 1

    print(f"{fruit.capitalize():8} : {count} shape images")


print("--------------------------------")
print("Shape dataset created successfully!")
print("--------------------------------")