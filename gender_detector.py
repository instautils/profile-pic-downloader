import cv2
import dlib
import os
import pickle
import sys
from tqdm import tqdm
from glob import glob
from shutil import copyfile

target_directory = 'labels'

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(
    os.path.join("models", "shape_predictor_68_face_landmarks.dat")
)
recognizer = dlib.face_recognition_model_v1(
    os.path.join("models", "dlib_face_recognition_resnet_model_v1.dat")
)
classifier = pickle.load(open(os.path.join('models', 'gender.pickle'), 'r'))


def predict_gender(encoding):
    result = classifier(dlib.vector(encoding))
    if result > 0.4:
        return "male"
    if result < -0.4:
        return "female"
    return "unknown"


def face_descriptor(img, rect):
    return recognizer.compute_face_descriptor(img, predictor(img, rect), 1)


def face_size(face_rect):
    return face_rect.width() * face_rect.height()


def detect_gender_of_image(image_file):
    try:
        image = cv2.imread(image_file)
    except Exception:
        return []

    image = cv2.resize(image, (256, 256))
    dets, scores, _ = detector.run(image, 1, -1)
    if not dets:
        return []
    if sum(scores) < 0.1:
        return []

    faces = list(dets)
    faces.sort(cmp=lambda x, y: face_size(y) - face_size(x))
    face = faces[0]
    description = face_descriptor(image, face)
    return predict_gender(description)


def do_process(image_file):
    target_file = os.path.basename(image_file)
    gender = detect_gender_of_image(image_file)
    if gender == 'unknown':
        return

    path = os.path.join(
        target_directory,
        gender,
        target_file,
    )
    if os.path.exists(path):
        return

    copyfile(image_file, path)


for image_file in glob('images/*.jpg'):
    do_process(image_file)
