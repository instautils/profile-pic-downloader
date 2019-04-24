import cv2
import dlib
import os
import multiprocessing
from tqdm import tqdm
from glob import glob

detector = dlib.get_frontal_face_detector()


def check_image(image_file):
    try:
        image = cv2.imread(image_file)
    except BaseException:
        os.remove(image_file)
        return 1

    image = cv2.resize(image, (256, 256))
    dets, _, _ = detector.run(image, 1, -1)
    if len(dets) == 0:
        os.remove(image_file)
        return 1
    return 0


pool = multiprocessing.Pool(processes=8)
results = [pool.apply(check_image, args=(image_file,))
           for image_file in glob('images/*.jpg')]

print "{} files removed !".format(sum(results))
