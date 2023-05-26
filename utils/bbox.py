import argparse
import os
import random

import cv2

import utils

"""
Used for checking bounding boxes on the images after preparations (mask to yolo, coco to yolo, resize) etc.

To show specific image with bounding boxes:
    python bbox.py image -i <image path> -a <annotation path>
To show random images with bounding boxes consecutively:
    python bbox.py random -i <image folder> -a <annotation folder>
To process all images in a folder and saving them to a output folder:
    python bbox.py bulk -i <image folder> -a <annotation folder> -o <output folder>
"""

def process_all_images(image_folder, annot_folder, output_folder):
    image_paths = list(
        map(lambda x: os.path.join(image_folder, x), os.listdir(image_folder))
    )

    for image_path in image_paths:
        image_name = os.path.basename(image_path)
        annot_path = os.path.join(
            annot_folder, "{}.txt".format(image_name.split(".")[0])
        )
        target_image_path = os.path.join(output_folder, image_name)
        image = get_bbox_image(image_path, annot_path)
        cv2.imwrite(target_image_path, image)


def plot_random_images(image_folder, annot_folder):
    basenames = list(
        map(lambda x: os.path.basename(x).split(".")[0], os.listdir(image_folder))
    )
    while True:
        sample = random.choice(basenames)
        image_path = os.path.join(image_folder, "{}.jpg".format(sample))
        annot_path = os.path.join(annot_folder, "{}.txt".format(sample))
        plot_image(image_path, annot_path)


def plot_image(image_path, annot_path):
    image = get_bbox_image(image_path, annot_path)
    cv2.imshow(os.path.basename(image_path), image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_bbox_image(image_path, annot_path):
    image = cv2.imread(image_path)
    with open(annot_path, "r") as f:
        object_lines = list(map(lambda x: x.strip(), f.readlines()))

    for line in object_lines:
        _, x, y, w, h = map(lambda x: float(x), line.split(" "))
        H, W, D = image.shape
        x = x * W
        y = y * H
        w = w * W
        h = h * H
        x = x - (w / 2)
        y = y - (h / 2)
        x1 = int(x)
        y1 = int(y)
        x2 = int(x + w)
        y2 = int(y + h)
        cv2.rectangle(image, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)

    return image


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True, dest="mode")

    # subparser for image
    subparser_image = subparsers.add_parser("image", help="plot specific image")
    subparser_image.add_argument("-i", "--image_path", help="image path")
    subparser_image.add_argument("-a", "--annot_path", help="annotation path")

    # subparser for random
    subparser_random = subparsers.add_parser(
        "random", help="plot random images consecutively"
    )
    subparser_random.add_argument("-i", "--image_folder", help="image folder")
    subparser_random.add_argument("-a", "--annot_folder", help="annotation folder")

    # subparser for image
    subparser_bulk = subparsers.add_parser(
        "bulk", help="draw bboxes on all images and save them to output file"
    )
    subparser_bulk.add_argument("-i", "--image_folder", help="image folder")
    subparser_bulk.add_argument("-a", "--annot_folder", help="annotation folder")
    subparser_bulk.add_argument("-o", "--output_folder", help="annotation folder")

    args = parser.parse_args()

    if args.mode == "image":
        print("Mode: Image [plot specific image]")
        print("Image Path:", args.image_path)
        print("Annotation Path:", args.annot_path)
        plot_image(utils.get_path(args.image_path), utils.get_path(args.annot_path))
    elif args.mode == "random":
        print("Mode: Random [plot random images consecutively]")
        print("Image Folder:", args.image_folder)
        print("Annotation Folder:", args.annot_folder)
        plot_random_images(
            utils.get_path(args.image_folder), utils.get_path(args.annot_folder)
        )
    elif args.mode == "bulk":
        print("Mode: Bulk [draw bbox on all images and save]")
        print("Image Folder:", args.image_folder)
        print("Annotation Folder:", args.annot_folder)
        print("Output Folder:", args.output_folder)
        process_all_images(
            utils.get_path(args.image_folder),
            utils.get_path(args.annot_folder),
            utils.get_path(args.output_folder),
        )
    else:
        pass
