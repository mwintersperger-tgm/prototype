import json


def parseline(line):
    if line[len(line) - 2] == ',':
        return json.loads(line[:-2])
    else:
        return json.loads(line)


def parsefirstline(line):
    obj = json.loads(line + ']}')
    obj.pop('values')
    return obj