import csv
import json
import os
import exportPkg.merge as Merge
import pandas
import importPkg.util as util


def forward(dataset, file):
    """
    writes a new line of data to the output file
    :param dataset:
    :param file:
    :return:
    """
    with open(file, "a") as outfile:
        try:
            for x in dataset.keys():
                s = dataset[x]
                if isinstance(s, str):
                    dataset[x] = s.replace('"', "''").strip()
            outfile.write(json.dumps(dataset) + ",\n")
            outfile.close()
            print(json.dumps(dataset))
        except Exception as err:
            print(str(err))
    pass


def start_file(file, countrycode=0, lockedrows=list(), displayname="Sample Table", ruleset=""):
    """
    writes the first line of the data file
    :param file:
    :param countrycode:
    :param lockedrows:
    :param displayname:
    :return:
    """
    with open(file, "w") as outfile:
        outfile.truncate(0)
        outfile.write('{"rules":"' + str(ruleset) + '", "cc":"' + str(countrycode) + '", "locked":' + json.dumps(lockedrows) + ', "tablename":"' + displayname + '", "values":[ \n')


def validatemapping(mapping):
    """
    checks if a mapping has the appropriate structure. This means that each key has
    :param mapping:
    :return:
    """
    if not isinstance(mapping, dict):
        return False

    dupe = []
    for x in mapping.keys():
        if x != '__locked__':
            if not isinstance(mapping[x], str):
                return False
            else:
                if mapping[x] in dupe:
                    return False
                else:
                    dupe.append(mapping[x])

    try:
        if not isinstance(mapping['__locked__'], list):
            return False
    except Exception as err:
        print(err)
        return False

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
    """
    legacy method, isn't usable with mappings and country codes
    :param args:
    :return:
    """
    cfg = {}
    try:
        with open("../resources/inconfig.json") as file:
            cfg = json.load(file)
    except Exception as err:
        print(err)
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


def importcsv(infile, outfile, delim, mappingname=None, countrycode=0, displayname = "Sample Table", ruleset=""):
    """
    Imports the infile (CSV) into a JSON structure that should be usable for the rest of the project.
    The JSON will be saved in the outfile.
    The default delimiter is ';', but it can be changed.
    if mapping is used, it should have the following structure: {"colname" = "mappedname", "colname2" = "mappedname2", [..]}
    countrycode is needed to assign a cc to the file (can be left empty)
    :param infile:
    :param outfile:
    :param delim:
    :param mappingname:
    :param countrycode:
    :param displayname:
    :return:
    """
    with open(infile) as file:
        if mappingname is not None:
            mapping = loadmapping(mappingname)
        else:
            mapping = None
        locked = list()
        if mapping is not None:
            locked = mapping['__locked__']
            mapping.pop('__locked__')
        start_file(outfile, countrycode, locked, displayname, ruleset)
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
                        if mapping is not None:
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


def importxlsx(infile, outfile, mappingname=None, countrycode=0, displayname = "Sample Table", ruleset=""):
    """
    imports data from an .xlsx and adapts it into the internally used JSON structure. Due to the way pandas internally
    works, this isn't particularly memory conserving
    :param infile:
    :param outfile:
    :param countrycode
    :param displayname
    :param lockedrows
    :return:
    """
    if mappingname is not None:
        mapping = loadmapping(mappingname)
    else:
        mapping = None
    lockedrows = list()
    if mapping is not None:
        lockedrows = mapping['__locked__']
        mapping.pop('__locked__')
    newfile = pandas.ExcelFile(infile)
    file = pandas.read_excel(open(infile, 'r'), sheet_name=newfile.sheet_names[0])
    data = file.to_dict()
    print('\n' + str(data))
    keys = data.keys()
    keyslength = 0
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
            z = y.strip()
            obj[z] = dict()
            obj[z]['value'] = data[z][num]
            obj[z]['validated'] = False
        arr.append(obj)
    print(arr)
    start_file(outfile, countrycode, lockedrows, displayname, ruleset)
    for x in arr:
        forward(x, outfile)
    end_file(outfile)


def importxlsxmerge(infile, outfile, keyset):
    """
    Does the same as the other xlsx import, but with the slight difference that it assumes that there's already a JSON
    structure at the outfile location. I recommend checking if a file exists at the "outfile" location and then use
    either this method or importxlsx.
    :param infile:
    :param outfile:
    :param keyset:
    :return:
    """
    newfile = pandas.ExcelFile(infile)
    file = pandas.read_excel(open(infile, 'rb'), sheet_name=newfile.sheet_names[0])
    data = file.to_dict()
    print('\n' + str(data))
    keys = data.keys()
    keyslength = 0
    for x in keys:
        keyslength = data[x].keys()
        break
    length = len(keyslength)
    # print(length)
    # print(keys)
    arr = list()
    for num in range(0, length):
        obj = dict()
        for y in keys:
            z = y.strip()
            obj[z] = dict()
            obj[z]['value'] = data[z][num]
            obj[z]['validated'] = False
        arr.append(obj)
    print(arr)
    prevarr = list()
    with open(outfile) as file:
        string = file.readline()
        obj = util.parsefirstline(string)
        try:
            while True:
                prevarr.append(util.parseline(file.readline()))
        except Exception as err:
            print(err)
    for x in prevarr:
        align = False
        for y in arr:
            if Merge.keyalign(x, y, keyset):
                align = True
                x = Merge.mergelinerisky([y, x])
                break
        if not align:
            arr.append(x)
    start_file(outfile, obj['cc'], obj['locked'], obj['tablename'], obj['rules'])
    for x in arr:
        forward(x, outfile)
    end_file(outfile)
