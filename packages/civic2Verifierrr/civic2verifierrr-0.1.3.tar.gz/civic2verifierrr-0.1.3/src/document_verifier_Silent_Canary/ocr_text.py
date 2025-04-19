from ultralytics import YOLO
import cv2
import pytesseract
import json

def extract_front_fields(img_path, model_path="best.pt"):
    model = YOLO(model_path)
    results = model(img_path)[0]
    class_map = {
        0: "uid",
        1: "dob",
        2: "gender",
        3: "name"
    }
    image = cv2.imread(img_path)
    fields = {}
    for box in results.boxes:
        cls_id = int(box.cls[0])
        field_name = class_map.get(cls_id, f"class_{cls_id}")
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        crop = image[y1:y2, x1:x2]
        text = pytesseract.image_to_string(crop, lang="eng+hin").strip()
        fields[field_name] = text
    return fields

def extract_back_address(img_path, model_path="best_back.pt"):
    model = YOLO(model_path)
    results = model(img_path)[0]
    image = cv2.imread(img_path)
    address = ""
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        crop = image[y1:y2, x1:x2]
        address = pytesseract.image_to_string(crop, lang="eng+hin").strip()
        break
    address = address.replace("Address:", "").strip()
    return {"address": address}

def get_ocr_data(front_img_path,back_img_path):
  #  front_img = "aadharfront.png"
##    back_img = "adhaarback.png"

    front_fields = extract_front_fields(front_img_path)
    back_fields = extract_back_address(back_img_path)
    combined = {**front_fields, **back_fields}
    return combined
#print("extracted fields : \n", json.dumps(combined, indent=2))
