import os
import json

#functions

def load_json(path):
    with open(path, encoding="utf-8", errors="ignore") as file:
        data = json.load(file)
    return data

#run

json_path = "data/austraits/traits_nsw.json"
json_file = load_json(json_path)


print(json_file[0]["trait_name"])
print(json_file[0].keys())

# for sp in json_file:
#     # sp_name = sp["taxon_name"]
#     traits = len(sp.keys())
#     print(f"traits: {traits}")