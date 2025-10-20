import json

def writeJson(filename, data):
    with open(filename, "w", encoding = "utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii = False, indent = 2, separators = (", ", ": "))

def readJson(filename):
    with open(filename) as file:
        content = file.read()
    output = json.loads(content)
    return output