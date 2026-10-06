import os

dataset_path = "dataset/fruit"

classes = [
    "apple",
    "banana",
    "mango",
    "orange",
    "unknown"
]

total = 0

print("\nFRUIT DATASET CHECK")
print("-" * 30)

for class_name in classes:

    folder = os.path.join(
        dataset_path,
        class_name
    )

    if os.path.exists(folder):

        count = len([
            file for file in os.listdir(folder)
            if file.lower().endswith(
                (".jpg", ".jpeg", ".png")
            )
        ])

        print(f"{class_name:10} : {count}")
        total += count

    else:
        print(f"{class_name:10} : Folder not found")

print("-" * 30)
print(f"Total      : {total}")