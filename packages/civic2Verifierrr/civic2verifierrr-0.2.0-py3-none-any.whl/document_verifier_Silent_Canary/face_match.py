# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 01:00:36 2025

@author: advit
"""
import face_recognition
import cv2

def extract_face_from_doc(doc_path):
    card_img=face_recognition.load_image_file(doc_path)
    face_locations=face_recognition.face_locations(card_img)
    if  not face_locations:
        raise Exception("No face found in the image")
        
    top,right,bottom,left=face_locations[0]
    card_face=card_img[top:bottom,left:right]
    cv2.imwrite("aadhar_face_crop.jpg", cv2.cvtColor(card_face, cv2.COLOR_RGB2BGR))

def capture_live_selfie():
    cam = cv2.VideoCapture(0)
    print("📸 Press 's' to capture selfie")
    while True:
        ret, frame = cam.read()
        cv2.imshow("Live Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite("live_selfie.jpg", frame)
            break
    cam.release()
    cv2.destroyAllWindows()

    selfie_img = face_recognition.load_image_file("live_selfie.jpg")
    selfie_faces = face_recognition.face_locations(selfie_img)

    if not selfie_faces:
        raise Exception("❌ No face found in selfie")

    top, right, bottom, left = selfie_faces[0]
    selfie_face = selfie_img[top:bottom, left:right]
    cv2.imwrite("live_selfie_crop.jpg", cv2.cvtColor(selfie_face, cv2.COLOR_RGB2BGR))

def match_faces():
    aadhaar_face = face_recognition.load_image_file("aadhar_face_crop.jpg")
    selfie_face = face_recognition.load_image_file("live_selfie_crop.jpg")

    aadhaar_enc = face_recognition.face_encodings(aadhaar_face)[0]
    selfie_enc = face_recognition.face_encodings(selfie_face)[0]

    match = face_recognition.compare_faces([aadhaar_enc], selfie_enc)[0]

    print("✅ MATCHED" if match else "❌ NOT MATCHED")
    return match
def match_face_pipeline(img_path):
    doc_face_path = extract_face_from_doc(img_path)
    selfie_face_path = capture_live_selfie()
    result = match_faces()
    return result