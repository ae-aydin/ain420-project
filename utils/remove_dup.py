import os
import sys

import imagehash
from PIL import Image

import utils

"""
Used for removing duplicate images in the dataset.
"""

def find_image_duplicates(image_folder):
    files = list(map(lambda x: os.path.join(image_folder, x), os.listdir(image_folder)))
    hash_dict = {}
    duplicates = []

    for file in files:
        image = Image.open(file)
        image_hash = imagehash.phash(image)

        if image_hash in hash_dict:
            duplicates.append(file)
        else:
            hash_dict[image_hash] = file

    return duplicates


def remove_duplicates(image_folder, annot_folder, dupli_folder):
    duplicate_images = find_image_duplicates(image_folder)
    duplicate_annots = list(
        map(
            lambda x: os.path.join(
                annot_folder, "{}.txt".format(os.path.basename(x).split(".")[0])
            ),
            duplicate_images,
        )
    )
    print("Duplicate images found: {}".format(len(duplicate_images)))
    if len(duplicate_images) == 0:
        print("Terminating...")
        sys.exit()
    else:
        opt_input = str(input("Do you want to continue? [y]/[n]:"))
        if opt_input == "y":
            dataset_name = image_folder.split("\\")[-2]
            dupli_current_folder = os.path.join(dupli_folder, "{}_dup".format(dataset_name))
            dupli_image_folder = os.path.join(dupli_current_folder, "images")
            dupli_annot_folder = os.path.join(dupli_current_folder, "annotations")
            try:
                utils.make_directory(dupli_current_folder)
                utils.make_directory(dupli_image_folder)
                utils.make_directory(dupli_annot_folder)
            except:
                raise FileExistsError
            utils.copy_remove(duplicate_images, dupli_image_folder)
            utils.copy_remove(duplicate_annots, dupli_annot_folder)
        elif opt_input == "n":
            print("Terminating...")
            sys.exit()
        else:
            pass


if __name__ == "__main__":
    image_folder = os.path.normpath(sys.argv[1])  # image folder
    annot_folder = os.path.normpath(sys.argv[2])  # annotation folder
    dupli_folder = os.path.normpath(
        sys.argv[3]
    )  # folder to copy duplicate files in order to inspect them
    remove_duplicates(image_folder, annot_folder, dupli_folder)
