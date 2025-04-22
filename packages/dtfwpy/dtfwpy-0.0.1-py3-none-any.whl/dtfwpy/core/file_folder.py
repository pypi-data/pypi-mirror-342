import os


def make_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def folder_path_of_file(path):
    return os.path.dirname(os.path.realpath(path))


def remove_file(path):
    if os.path.exists(path):
        os.remove(path)
