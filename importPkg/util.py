import json
import os

def parseline(line):
    if line[len(line) - 2] == ',':
        return json.loads(line[:-2])
    else:
        return json.loads(line)


def parsefirstline(line):
    obj = json.loads(line + ']}')
    obj.pop('values')
    return obj


def fetchtablenames(folder):
    onlyfiles = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    for x in onlyfiles:
        print(x)
