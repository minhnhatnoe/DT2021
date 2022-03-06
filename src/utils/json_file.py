'''Module for working with json'''
from os import environ
import json
from dotenv import load_dotenv

def load_from_json(filepath: str) -> dict:
    load_dotenv()
    path = environ.get("DATAPATH")

    with open(f"{path}{filepath}.json", "r") as file:
        json_data = json.load(file)
        return json_data

def write_to_json(filepath: str, data: dict):
    load_dotenv()
    path = environ.get("DATAPATH")

    with open(f"{path}{filepath}.json", "w") as file:
        file.seek(0)
        json.dump(data, file)
        file.truncate()