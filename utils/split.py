import os
import shutil
import sys

import numpy as np

import utils

"""
Used for splitting the data and the image folder into training, validation, and test sets according to YOLO requirements.
Train: %75
Validation: %10
Test: %15
"""

def split(image_folder, annot_folder, target_data_folder):
    data_image_folder = os.path.join(target_data_folder, "images")
    data_image_train_folder = os.path.join(data_image_folder, "train")
    data_image_val_folder = os.path.join(data_image_folder, "val")
    data_image_test_folder = os.path.join(data_image_folder, "test")
    data_label_folder = os.path.join(target_data_folder, "labels")
    data_label_train_folder = os.path.join(data_label_folder, "train")
    data_label_val_folder = os.path.join(data_label_folder, "val")
    data_label_test_folder = os.path.join(data_label_folder, "test")

    try:
        utils.make_directory(data_image_folder)
        utils.make_directory(data_image_train_folder)
        utils.make_directory(data_image_val_folder)
        utils.make_directory(data_image_test_folder)
        utils.make_directory(data_label_folder)
        utils.make_directory(data_label_train_folder)
        utils.make_directory(data_label_val_folder)
        utils.make_directory(data_label_test_folder)
    except:
        raise

    basename_list = list(map(lambda x: x.split(".")[0], os.listdir(image_folder)))
    np.random.shuffle(basename_list)

    train_count = int(0.75 * len(basename_list))
    test_count = int(0.15 * len(basename_list))
    val_count = len(basename_list) - train_count - test_count

    assert train_count + val_count + test_count == len(basename_list)

    train_selected = basename_list[:train_count]
    test_selected = basename_list[train_count : train_count + test_count]
    val_selected = basename_list[train_count + test_count :]

    assert len(set(train_selected).intersection(set(test_selected))) == 0
    assert len(set(train_selected).intersection(set(val_selected))) == 0
    assert len(set(test_selected).intersection(set(val_selected))) == 0

    transfer(
        train_selected,
        image_folder,
        annot_folder,
        data_image_train_folder,
        data_label_train_folder,
    )
    transfer(
        test_selected,
        image_folder,
        annot_folder,
        data_image_test_folder,
        data_label_test_folder,
    )
    transfer(
        val_selected,
        image_folder,
        annot_folder,
        data_image_val_folder,
        data_label_val_folder,
    )


def transfer(split, source_image, source_annot, target_image, target_annot):
    for element in split:
        element_image = os.path.join(source_image, "{}.jpg".format(element))
        element_annot = os.path.join(source_annot, "{}.txt".format(element))
        element_target_image = os.path.join(target_image, "{}.jpg".format(element))
        element_target_annot = os.path.join(target_annot, "{}.txt".format(element))
        shutil.copy2(element_image, element_target_image)
        shutil.copy2(element_annot, element_target_annot)


if __name__ == "__main__":
    image_folder = os.path.normpath(sys.argv[1])  #  image folder
    annot_folder = os.path.normpath(sys.argv[2])  #  annotations folder
    target_data_folder = os.path.normpath(sys.argv[3])  # target data folder
    split(image_folder, annot_folder, target_data_folder)
