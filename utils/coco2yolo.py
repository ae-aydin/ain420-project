import json
import os
import sys

import pandas as pd

import utils

"""
Used for converting annotations in COCO format to YOLO format.
"""

class COCO2YOLO:
    def __init__(self, annot_file):
        self.annot_file = annot_file
        self.read()

    def read(self):
        with open(self.annot_file, "r") as f:
            json_data = json.load(f)
        self.annotations = pd.json_normalize(json_data, record_path=["annotations"])
        self.images = pd.json_normalize(json_data, record_path=["images"])
        self.categories = pd.json_normalize(json_data, record_path=["categories"])

    def convert(self, target_folder, name_status):
        output_dict = dict()
        self.annotations.loc[self.annotations["category_id"] == 1, "category_id"] = 0
        file_names = self.images["file_name"].unique()

        for file in file_names:
            current_image = self.images.loc[self.images["file_name"] == file]
            id = current_image["id"].values[0]
            H = current_image["height"].values[0]
            W = current_image["width"].values[0]
            boxes = self.annotations.loc[self.annotations["image_id"] == id]
            dict_value = list()
            for b in boxes["bbox"]:
                x = (b[0] + (b[2] / 2)) / W
                y = (b[1] + (b[3] / 2)) / H
                w = b[2] / W
                h = b[3] / H
                dict_value.append(
                    "{} {:.6f} {:.6f} {:.6f} {:.6f}".format(
                        0, x, y, w, h
                    )
                )
            output_dict[file.split(".")[0]] = "\n".join(dict_value)

        for file in output_dict.keys():
            if name_status:
                file_path = os.path.join(target_folder, utils.rename(file, "b", "txt"))
            else:
                file_path = os.path.join(target_folder, "{}.txt".format(file))
            with open(file_path, "w") as f:
                f.write(output_dict[file])


if __name__ == "__main__":
    main_json_file = os.path.normpath(sys.argv[1])  # json file
    target_folder = os.path.normpath(sys.argv[2])  # target folder
    name_status = sys.argv[3].lower() == "true"
    converter = COCO2YOLO(main_json_file)
    converter.convert(target_folder, name_status)
