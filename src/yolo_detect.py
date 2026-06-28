import os
import csv
from ultralytics import YOLO
from collections import defaultdict

# =========================
# LOAD MODEL
# =========================
model = YOLO("yolov8n.pt")

IMAGE_DIR = "data/raw/images"
OUTPUT_FILE = "data/yolo_results.csv"

results_data = []

# COCO classes we care about
PERSON_CLASS = "person"
PRODUCT_CLASSES = ["bottle", "cup", "cell phone", "box", "container"]

# =========================
# CLASSIFY IMAGE FUNCTION
# =========================
def classify(objects):
    has_person = any(obj == "person" for obj in objects)
    has_product = any(obj in PRODUCT_CLASSES for obj in objects)

    if has_person and has_product:
        return "promotional"
    elif has_product and not has_person:
        return "product_display"
    elif has_person and not has_product:
        return "lifestyle"
    else:
        return "other"

# =========================
# SCAN IMAGES
# =========================
for root, dirs, files in os.walk(IMAGE_DIR):
    for file in files:
        if file.endswith(".jpg") or file.endswith(".png"):

            image_path = os.path.join(root, file)
            message_id = file.split(".")[0]

            # RUN YOLO
            result = model(image_path)[0]

            detected_objects = []
            confidences = []

            for box in result.boxes:
                cls_id = int(box.cls[0])
                name = model.names[cls_id]
                conf = float(box.conf[0])

                detected_objects.append(name)
                confidences.append(conf)

            image_category = classify(detected_objects)

            results_data.append({
                "message_id": message_id,
                "image_path": image_path,
                "objects": ",".join(detected_objects),
                "confidence": round(sum(confidences)/len(confidences), 2) if confidences else 0,
                "category": image_category
            })

# =========================
# SAVE CSV
# =========================
os.makedirs("data", exist_ok=True)

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results_data[0].keys())
    writer.writeheader()
    writer.writerows(results_data)

print("YOLO detection completed. Results saved to:", OUTPUT_FILE)