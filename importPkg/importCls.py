import csv
import json
import os
from pandas import DataFrame
import pandas


def forward(dataset, file):
    with open(file, "a") as outfile:
        try:
            outfile.write(json.dumps(dataset) + ",\n")
            outfile.close()
            print(json.dumps(dataset))
        except Exception as err:
            print(str(err))
    pass


def start_file(file):
    with open(file, "w") as outfile:
        outfile.truncate(0)
        outfile.write('{"rules":"", "cc":"", "values":[\n')


def validatemapping(mapping):
    """
    checks if a mapping has the appropriate structure
    :param mapping:
    :return:
    """
    if not isinstance(mapping, dict):
        return False

    dupe = []
    for x in mapping.keys():
        if not isinstance(mapping[x], str):
            return False
        else:
            if mapping[x] in dupe:
                return False
            else:
                dupe.append(mapping[x])

    return True


def savemapping(mapping, outfile):
    """
    safes the mapping at the given path (outfile)
    :param mapping:
    :param outfile:
    :return:
    """

    if not validatemapping(mapping):
        return False

    if len(mapping.keys()) == 0:
        return False

    with open(outfile, "w") as file:
        file.truncate(0)
        file.write(json.dumps(mapping))
        return True


def loadmapping(infile):
    """
    returns the mapping at the given relative path. If the mapping isn't valid, returns None
    :param mapping:
    :param infile:
    :return:
    """

    with open(infile, "r") as file:
        tmp = json.loads(file.read())
        if not validatemapping(tmp):
            return None
        return tmp


def end_file(file):
    with open(file, "a") as outfile:
        outfile.truncate(os.path.getsize(file) - 3)
        outfile.write('\n]}')


def importcsv2(args):
    cfg = {}
    with open("../resources/inconfig.json") as file:
        cfg = json.load(file)
    if isinstance(cfg['delimiter'], int):
        cfg['delimiter'] = chr(cfg['delimiter'])
    if len(args.delimiter) > 0:
        cfg['delimiter'] = args.delimiter
    if len(args.fileinput) > 0:
        cfg['file'] = args.fileinput
    if len(args.fileoutput) > 0:
        cfg['out'] = args.fileoutput
    with open(cfg['file']) as file:
        start_file(cfg['out'])
        colnames = []
        read = csv.reader(file, delimiter=cfg['delimiter'])
        count = 0
        firstline = True
        for row in read:
            if firstline:
                firstline = False
                colnames.append(row)
                print(colnames)
            else:
                temp = row
                res = {}
                if row:
                    for x in range(0, len(temp)):
                        res[colnames[0][x]] = {}
                        res[colnames[0][x]]["value"] = temp[x]
                        res[colnames[0][x]]["validated"] = False
                    forward(res, cfg['out'])
                    count += 1
        end_file(cfg['out'])
        print(str(count) + " lines imported")


def importcsv(infile, outfile, delim, mappingname = None):
    """
    Imports the infile (CSV) into a JSON structure that should be usable for the rest of the project.
    The JSON will be saved in the outfile.
    The default delimiter is ';', but it can be changed.
    if mapping is used, it should have the following structure: {"colname" = "mappedname", "colname2" = "mappedname2", [..]}
    :param infile:
    :param outfile:
    :param delim:
    :param mappingname:
    :return:
    """
    with open(infile) as file:
        if mappingname is not None:
            mapping = loadmapping(mappingname)

        start_file(outfile)
        colnames = []
        read = csv.reader(file, delimiter=delim)
        count = 0
        firstline = True
        for row in read:
            if firstline:
                firstline = False
                colnames.append(row)
                print(colnames)
            else:
                temp = row
                res = {}
                if row:
                    for x in range(0, len(temp)):
                        if mappingname is not None:
                            res[mapping[colnames[0][x]]] = {}
                            res[mapping[colnames[0][x]]]["value"] = temp[x]
                            res[mapping[colnames[0][x]]]["validated"] = False
                        else:
                            res[colnames[0][x]] = {}
                            res[colnames[0][x]]["value"] = temp[x]
                            res[colnames[0][x]]["validated"] = False
                    forward(res, outfile)
                    count += 1
        end_file(outfile)
        print(str(count) + " lines imported")


def importxlsx(infile, outfile):
    newfile = pandas.ExcelFile(infile)
    file = pandas.read_excel(open(infile, 'rb'), sheet_name=newfile.sheet_names[0])
    data = file.to_dict()
    print('\n' + str(data))
    keys = data.keys()
    for x in keys:
        keyslength = data[x].keys()
        break
    length = len(keyslength)
    print(length)
    print(keys)
    arr = list()
    for num in range(0, length):
        obj = dict()
        for y in keys:
            obj[y] = dict()
            obj[y]['value'] = data[y][num]
            obj[y]['validated'] = False
        arr.append(obj)
    print(arr)
    start_file(outfile)
    for x in arr:
        forward(x, outfile)
    end_file(outfile)
