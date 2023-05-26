import os
import shutil
import sys

import cv2
import numpy as np

import utils

"""
Used for converting pixel level annotation (mask) to YOLO format.
Specifically used for beachlitter dataset: https://www.seanoe.org/data/00743/85472/
Red areas: artificial litter
Pink areas: natural litter
"""

def get_eligible_images(bbox_folder, images_folder, filtered_images_folder):
    image_paths = [
        utils.get_filepath(images_folder, utils.get_basename(file_name), ext="jpg")
        for file_name in os.listdir(bbox_folder)
    ]
    for path in image_paths:
        shutil.copy2(path, filtered_images_folder)


def prep_bbox_yolo(mask_folder, bbox_folder):
    filepath_list = [
        os.path.join(mask_folder, file_name) for file_name in os.listdir(mask_folder)
    ]
    for file in filepath_list:
        image = prep_image(file)
        H, W = image.shape
        cnts = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        if len(cnts) == 0:
            continue
        with open(utils.get_filepath(bbox_folder, utils.get_basename(file)), "w") as f:
            for c in cnts:
                x, y, w, h = cv2.boundingRect(c)
                x = (x + (w / 2)) / W
                y = (y + (h / 2)) / H
                w = w / W
                h = h / H
                f.write(
                    "0 {:.6f} {:.6f} {:.6f} {:.6f}\n".format(x, y, w, h)
                )


def prep_image(img_path):
    image = cv2.imread(img_path)
    red_mask = np.all(image == [0, 0, 128], axis=-1).astype(np.uint8) * 255
    image = cv2.bitwise_and(image, image, mask=red_mask)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    (T, threshold_image) = cv2.threshold(image, 10, 255, cv2.THRESH_BINARY)
    return threshold_image


if __name__ == "__main__":
    image_folder = os.path.normpath(sys.argv[1])  # image folder
    mask_folder = os.path.normpath(sys.argv[2])  # mask folder
    target_bbox_folder = os.path.normpath(sys.argv[3])  # target bbox folder
    filtered_images_folder = os.path.normpath(sys.argv[4])  # filtered images folder
    prep_bbox_yolo(mask_folder, target_bbox_folder)
    get_eligible_images(target_bbox_folder, image_folder, filtered_images_folder)
