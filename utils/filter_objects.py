import os
import sys

import utils

"""
Used for removing too small objects' annotations and deleting overcrowded images. 
"""

def filter_small_objects(
    annot_folder, new_annot_folder, image_folder, dump_folder, image_size=(640, 640)
):
    file_list = list(
        map(lambda x: os.path.join(annot_folder, x), os.listdir(annot_folder))
    )
    removed_object_count = 0
    object_count = 0
    empty_images = list()

    for file_path in file_list:
        suitable_objects = list()

        with open(file_path, "r") as f:
            bboxes = f.readlines()
            for bbox in bboxes:
                object_count += 1
                label, x, y, w, h = map(lambda x: float(x), bbox.strip().split(" "))
                bbox_width, bbox_height = int(w * image_size[0]), int(h * image_size[1])
                area = bbox_width * bbox_height
                if area >= 50:
                    suitable_objects.append(bbox.strip())
                else:
                    removed_object_count += 1

        if ((len(suitable_objects) == 0) or (len(suitable_objects) > 75)):
            image_name = "{}.jpg".format(os.path.basename(file_path).split(".")[0])
            image_path = os.path.join(image_folder, image_name)
            empty_images.append(image_path)
            removed_object_count += len(suitable_objects)
        else:
            with open(
                os.path.join(new_annot_folder, os.path.basename(file_path)), "w"
            ) as f:
                f.write("\n".join(suitable_objects))

    target_image_folder_path = os.path.join(
        dump_folder, "{}_empty".format(os.path.basename(image_folder))
    )
    try:
        utils.make_directory(target_image_folder_path)
    except:
        raise FileExistsError

    utils.copy_remove(empty_images, target_image_folder_path)

    print("Total images: {}".format(len(file_list)))
    print("Total objects: {}".format(object_count))
    print("Objects that are removed: {}".format(removed_object_count))
    print("Images that are removed: {}".format(len(empty_images)))
    print("Remaining images: {}".format(len(file_list) - len(empty_images)))
    print("Remaining total objects: {}".format(object_count - removed_object_count))


if __name__ == "__main__":
    annot_folder = os.path.normpath(sys.argv[1])
    new_annot_folder = os.path.normpath(sys.argv[2])
    image_folder = os.path.normpath(sys.argv[3])
    dump_folder = os.path.normpath(sys.argv[4])
    filter_small_objects(annot_folder, new_annot_folder, image_folder, dump_folder)


