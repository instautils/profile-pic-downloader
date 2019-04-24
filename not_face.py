import cv2
import dlib
import os
from tqdm import tqdm
from glob import glob

detector = dlib.get_frontal_face_detector()

counter = 0
for image_file in tqdm(glob('images/*.jpg')):
    try:
        image = cv2.imread(image_file)
    except BaseException:
        continue

    image = cv2.resize(image, (256, 256))
    dets, _, _ = detector.run(image, 1, -1)
    if len(dets) == 0:
        counter += 1
        os.remove(image_file)

print "{} files removed !".format(counter)