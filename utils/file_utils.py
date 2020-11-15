import codecs
import json


def saveJson(data, file_path):
    with codecs.open(file_path, mode="w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, default=lambda x: x.__dict__)


def load_json(file_path):
    with open(file_path, mode="r") as file:
        return json.load(file)
