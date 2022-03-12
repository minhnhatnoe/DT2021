'''Module for working with json'''
from os import environ
import json
from typing import Dict
from dotenv import load_dotenv


def load_from_json(filepath: str) -> Dict:
    '''Load file from json and returns dict'''
    load_dotenv()
    path = environ.get("DATAPATH")

    with open(f"{path}{filepath}.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)
        return json_data


def write_to_json(filepath: str, data: Dict):
    '''Write to json file'''
    load_dotenv()
    path = environ.get("DATAPATH")

    with open(f"{path}{filepath}.json", "w", encoding="utf-8") as file:
        file.seek(0)
        json.dump(data, file)
        file.truncate()
