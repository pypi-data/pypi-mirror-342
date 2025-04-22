import json
import os
from pathlib import Path

from jsonmerge import merge

downloads_path = str(Path.home() / "Downloads")

def writelines(file_name: str | Path, items: list):
    with open(file_name, 'w') as file:
        for i in range(0, len(items)):
            file.write(items[i]+"\n")

def readlines(file_name: str | Path) -> list:
    new_list = []

    with open(file_name, 'r') as file:
        for line in file.readlines():
            new_list.append(line.rstrip("\n"))

    return new_list

def read_file(path):
    if os.path.exists(path):
        with open(path, "r") as file:
            data = json.load(file)
        
        return data
    else:
         return None

def write_json(path, data):
    with open(path, "w") as file:
        json.dump(data, file, indent = 4)

def merge_json(path, new_data):
     current_data = read_file(path)
     
     merged_data = merge(current_data, new_data)
     
     write_json(path, merged_data)