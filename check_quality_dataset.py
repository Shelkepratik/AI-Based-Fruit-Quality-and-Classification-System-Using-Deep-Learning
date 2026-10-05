import os

base_path = "dataset/quality"

classes = ["good", "average", "poor"]

extensions = (".jpg", ".jpeg", ".png", ".webp")

total = 0

print("================================")
print("     QUALITY DATASET CHECK")
print("================================")

for quality in classes:

    folder = os.path.join(base_path, quality)

    count = 0

    for file in os.listdir(folder):

        if file.lower().endswith(extensions):
            count += 1

    total += count

    print(f"{quality.capitalize():8} : {count}")

print("--------------------------------")
print(f"Total    : {total}")
print("================================")