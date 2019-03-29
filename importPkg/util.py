import json
import os


def parseline(line):
    """
    Returns the proviced line of a data.json file as a string in the form of a dict.
    Throws an error if it's the first line, last line or an unrelated string that can't be parsed.
    :param line:
    :return:
    """
    if line[len(line) - 2] == ',':
        return json.loads(line[:-2])
    else:
        return json.loads(line)


def parsefirstline(line):
    """
    Returns the first line of a data.json file as a dict.
    The first line of a data.json file as a string should be provided as a parameter.
    :param line:
    :return:
    """
    obj = json.loads(line + ']}')
    obj.pop('values')
    return obj


def fetchtablenames(folder):
    """
    Extracts all table names found in the folder by taking the part between the .json ending and CC
    :param folder:
    :return:
    """
    onlyfiles = os.listdir(folder)
    output = list()
    for x in onlyfiles:
        lastnumindex = -1
        for i in range(0,len(x)):
            char = ord(list(x)[i])
            if char >= ord('0') and char <= ord('9'):
                lastnumindex = i
        if lastnumindex >= 0 and x.index('.') >= 0:
            output.append(x[lastnumindex+1:x.index('.json')])
    return output


def fetchdatafilenames(folder):
    """
    Returns all json files in the folder
    :param folder:
    :return:
    """
    onlyfiles = os.listdir(folder)
    for x in onlyfiles:
        if x.index('.json') < 0: onlyfiles.remove(x)
    return onlyfiles


def fetchtnameforfile(filename):
    """
    takes a filename and extracts the part between CC and file ending
    :param filename:
    :return:
    """
    lastnumindex = -1
    for i in range(0, len(filename)):
        char = ord(list(filename)[i])
        if char >= ord('0') and char <= ord('9'):
            lastnumindex = i
    if lastnumindex >= 0 and filename.index('.') >= 0:
        return filename[lastnumindex + 1:filename.index('.')]
