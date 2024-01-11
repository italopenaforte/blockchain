import json
import os


def save(data, file):
    blocks = read(file)

    for a in data:
        blocks.append(a)

    clean_file(file)

    with open(file, "a") as file:
        file.write(json.dumps(blocks))


def read(file):
    with open(file, "r") as file:
        blocks = file.read()

        if blocks:
            return json.loads(blocks)
        return []


def clean_file(file):
    with open(file, "w") as file:
        pass


def reset_file(file):
    clean_file(file)


class Database:
    def __init__(self):
        self._file_path = os.getenv("FILE_PATH")
        self._all_infos

    def connect(self):
        pass

    def commit(self):
        pass

    def insert(self):
        pass
