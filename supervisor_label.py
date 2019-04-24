import cv2
import os
import random
from glob import glob
from shutil import copyfile

target_directory = 'labels'

labels = {
    'm': 'male',
    'f': 'female',
    'u': 'unknown'
}


def random_string():
    return str(random.randint(100000, 999999))


for value in labels.values():
    path = os.path.join(target_directory, value)
    if not os.path.exists(path):
        os.makedirs(path)

image_list = glob(os.path.join('images', '*.jpg'))

index = 0
while index < image_list:
    image_file = image_list[index]
    target_file = os.path.basename(image_file)    
    image = cv2.imread(image_file)
    image = cv2.resize(image, (256, 256))

    cv2.imshow('image', image)
    key = cv2.waitKey(0) & 0xFF
    if key == 81:  # left arrow
        index -= 1
        if index < 0:
            index = 0
    elif key == ord('q'):
        break
    elif chr(key) in labels:
        path = os.path.join(
            target_directory,
            labels[chr(key)],
            target_file,
        )
        copyfile(image_file, path)
        os.remove(image_file)

        index += 1
