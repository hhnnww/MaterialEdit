import cv2
import face_recognition


def fun_人脸识别(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
    face_locations = face_recognition.face_locations(img)
    if len(face_locations) > 0:
        return True

    return False
