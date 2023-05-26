import os
import shutil

"""
Utility methods used in dataset preparation and preprocessing scripts.
"""

def make_directory(path):
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        raise FileExistsError


def copy_remove(dup_path_list, target_path):
    for dup_path in dup_path_list:
        dup_target_path = os.path.join(target_path, os.path.basename(dup_path))
        shutil.copy2(dup_path, dup_target_path)
        os.remove(dup_path)


def rename(image_name, prefix, ext):
    return "{}{}.{}".format(prefix, image_name.split(".")[0], ext)


def get_filepath(path, base, ext="txt"):
    return os.path.join(path, "{}.{}".format(base, ext))


def get_basename(file_path):
    base = os.path.basename(file_path)
    return os.path.splitext(base)[0]

def get_path(p):
    return os.path.normpath(p)
