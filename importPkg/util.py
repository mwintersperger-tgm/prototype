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

def fetchfilenames(folder):
    onlyfiles = os.listdir(folder)
    for x in onlyfiles:
        if x.index('.json') < 0: onlyfiles.remove(x)
    return onlyfiles

def fetchtnameforfile(filename):
    '''

    :param filename:
    :return:
    '''
    lastnumindex = -1
    for i in range(0, len(filename)):
        char = ord(list(filename)[i])
        if char >= ord('0') and char <= ord('9'):
            lastnumindex = i
    if lastnumindex >= 0 and filename.index('.') >= 0:
        return filename[lastnumindex + 1:filename.index('.')]
