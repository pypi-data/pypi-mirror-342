import json
from .qr import process_document
from .ocr_text import get_ocr_data
from .face_match import match_face_pipeline


    
def fields_match(data1,data2,fields):
    for field in fields:
        if data1.get(field,"").strip().lower()!=data2.get(field,"").strip().lower():
            return False
    return True

def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def verify_document(front_img, back_img,digilocker_json):
    digilocker_data =load_json_file(digilocker_json)
    verification_result = {
        "qr_decoded": False,
        "qr_match": False,
        "ocr_match": False,
        "face_match": False,
        "security_level": "Not Secure"
    }

    qr_data = process_document(back_img)
    if qr_data:
        verification_result["qr_decoded"] = True
        if fields_match(qr_data, digilocker_data, ["uid", "name", "address"]):
            verification_result["qr_match"] = True

    ocr_data = get_ocr_data(front_img,back_img)
    if fields_match(ocr_data, digilocker_data, ["uid", "name", "dob","gender","address"]):
        verification_result["ocr_match"] = True

    if match_face_pipeline(front_img):
        verification_result["face_match"] = True

    if verification_result["qr_match"] and verification_result["face_match"]:
        verification_result["security_level"] = "Very High"
    elif verification_result["qr_match"]:
        verification_result["security_level"] = "High"
    elif verification_result["ocr_match"] and verification_result["face_match"]:
        verification_result["security_level"] = "Medium-High"
    elif verification_result["ocr_match"]:
        verification_result["security_level"] = "Medium"

    return verification_result

if __name__=="__main__":
    front_img="aadharfront.png"
    back_img="adhaarback.png"
    digilocker_json="digilocker_json.json"
    verify_document(front_img, back_img, digilocker_json)
