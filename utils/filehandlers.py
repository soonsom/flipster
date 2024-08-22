import os
import json


def load_json(file_path):
    with open(os.path.abspath(file_path), 'r') as read_file:
        return json.load(read_file)


def make_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory
