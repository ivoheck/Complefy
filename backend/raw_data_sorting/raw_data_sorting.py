import re
import json

file_path = 'raw_modules.json'

with open(file_path, 'r', encoding='utf-8') as file:
    json_string = file.read()

modules = json_string.split('(modul)')
module = modules[1]

match_name = re.search(r"inhalte = (.*)", module)
if match_name:
    name = match_name.group(1)

print(name)

#print(module)

def modul_data(module):
    id = None
    name = None
    inhalte = None
    #id
    match_id = re.search(r"id = (.*)", module)
    if match_id:
        id = match_id.group(1)

    match_name = re.search(r"name = (.*)", module)
    if match_name:
        name = match_name.group(1)

    match_inhalte = re.search(r"inhalte = (.*)", module)
    if match_inhalte:
        inhalte = match_inhalte.group(1)

    