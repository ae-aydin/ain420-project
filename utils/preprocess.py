import os
import sys

import cv2

import utils

"""
Used for resizing images for training.
"""

def preprocess(image_folder, target_image_folder, name_status):
    images = os.listdir(image_folder)

    for image_name in images:
        image_path = os.path.join(image_folder, image_name)
        if name_status:
            target_image_path = os.path.join(
                target_image_folder, utils.rename(image_name, "b", "jpg")
            )
        else:
            target_image_path = os.path.join(target_image_folder, image_name)
        image = cv2.imread(image_path)
        image = resize(image)
        cv2.imwrite(target_image_path, image)


def resize(image, target_size=(640, 640)):
    return cv2.resize(image, target_size, interpolation=cv2.INTER_LINEAR)


if __name__ == "__main__":
    image_folder = os.path.normpath(sys.argv[1])  # path to folder containing images
    target_image_folder = os.path.normpath(sys.argv[2])  #  target image folder
    name_status = sys.argv[3].lower() == "true"
    preprocess(image_folder, target_image_folder, name_status)
