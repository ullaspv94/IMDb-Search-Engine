import os

import cv2

image_path = "images"


def save_faces(cascade, imgname):
    img = cv2.imread(os.path.join(image_path, imgname))
    for i, face in enumerate(cascade.detectMultiScale(img)):
        x, y, w, h = face
        sub_face = img[y:y + h, x:x + w]
        path = os.path.join("faces", "{}_{}.jpg".format(imgname, i))
        cv2.imwrite(path, sub_face)
        print (path)

if __name__ == '__main__':
    face_cascade = "haarcascade_frontalface_alt.xml"
    cascade = cv2.CascadeClassifier(face_cascade)
    # Iterate through files
    for f in [f for f in os.listdir(image_path) if os.path.isfile(os.path.join(image_path, f))]:
        print (f)
        save_faces(cascade, f)