import cv2
import dlib
import os
import pickle
import sys
import multiprocessing
from tqdm import tqdm
from glob import glob
from shutil import copyfile


class GenderDetector:
    def __init__(self):
        if not os.path.exists('models'):
            raise Exception('models directory does not exist')

        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(
            os.path.join("models", "shape_predictor_68_face_landmarks.dat")
        )
        self.recognizer = dlib.face_recognition_model_v1(
            os.path.join("models", "dlib_face_recognition_resnet_model_v1.dat")
        )
        self.classifier = pickle.load(
            open(os.path.join('models', 'gender.pickle'), 'r'))

    def face_size(self, rect):
        return rect.width() * rect.height()

    def predict_gender(self, encoding, thresh=0.4):
        result = self.classifier(dlib.vector(encoding))
        if result > thresh:
            return "male"
        if result < -thresh:
            return "female"
        return "unknown"

    def face_descriptor(self, img, rect):
        return self.recognizer.compute_face_descriptor(img, self.predictor(img, rect), 1)

    def process(self, image_file):
        image = cv2.imread(image_file)
        image = cv2.resize(image, (256, 256))
        dets, scores, _ = self.detector.run(image, 1, -1)
        if sum(scores) < 0.1:
            return 'unknown'

        faces = list(dets)
        faces.sort(cmp=lambda x, y: self.face_size(y) - self.face_size(x))
        face = faces[0]
        description = self.face_descriptor(image, face)
        return self.predict_gender(description)


def valid_image(image_file):
    with open(image_file, 'rb') as handler:
        string = handler.read(1)
        return len(string) != 0


def do_process(detector, image_file, target_directory='labels'):
    if not valid_image(image_file):
        return
        
    path = os.path.join(
        target_directory,
        detector.process(image_file),
        os.path.basename(image_file),
    )
    if os.path.exists(path):
        return

    copyfile(image_file, path)


if __name__ == "__main__":
    gender_detector = GenderDetector()

    pool = multiprocessing.Pool(processes=4)
    for image_file in glob('images/*.jpg'):
        pool.apply(do_process, args=(gender_detector, image_file))
