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
    onlyfiles = os.listdir(folder)
    print(onlyfiles)
    output = list()
    for x in onlyfiles:
        lastnumindex = -1
        for i in range(0,len(x)):
            char = ord(list(x)[i])
            if char >= ord('0') and char <= ord('9'):
                lastnumindex = i
        if lastnumindex >= 0 and x.index('.') >= 0:
            output.append(x[lastnumindex+1:x.index('.')])
    return output
