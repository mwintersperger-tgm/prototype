import csv
import json
import os


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
    '''
    checks if a mapping has the appropriate structure
    :param mapping:
    :return:
    '''
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
    '''
    safes the mapping at the given path (outfile)
    :param mapping:
    :param outfile:
    :return:
    '''

    if not validatemapping(mapping):
        return False

    if len(mapping.keys()) == 0:
        return False

    with open(outfile, "w") as file:
        file.truncate(0)
        file.write(json.dumps(mapping))
        return True


def loadmapping(infile):
    '''
    returns the mapping at the given relative path. If the mapping isn't valid, returns None
    :param mapping:
    :param infile:
    :return:
    '''

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
    :param mapping:
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

