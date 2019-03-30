import json
import csv
from pandas import DataFrame
import importPkg.util as util


def fetch(infile):
    """
    Return the ''values'' array for one data.json
    :param infile:
    :return:
    """
    try:
        with open(infile, "r") as sauce:
            obj = json.loads(sauce.read())
            return obj['values']
    except Exception as err:
        print(err)
        return None
    # TODO: receive data to export


def exportexcel(data, outfile):
    """
    Exports the given data, which should be a list of dictionaries (expect errors if it isn't one)
    as an excel file. The first row will feature the row names as bold text, all other rows will
    be filled with the data received from one of the dicts in the list.
    :param data: list of dicts
    :param outfile: filename
    :return:
    """
    tmp = {}
    firstset = True
    for x in data:
        if firstset:
            for y in x.keys():
                tmp[y] = []
            firstset = False
        for y in tmp.keys():
            try:
                tmp[y].append(x[y]["value"])
            except Exception as err:
                print(str(err))

    print(tmp)
    frame = DataFrame(tmp)
    frame.to_excel(outfile, sheet_name="test", index=False)


def exportcsv(data, outfile):
    """
    Exports the given data, which should be a list of dictionaries (expect errors if it isn't one)
    as a CSV file. First row includes the column names, all others include values
    :param data: list of dicts
    :param outfile: location of the file
    :return:
    """
    delimiter = ';'
    with open('../resources/outconfig.json') as file:
        try:
            conf = json.loads(file.read())
            delimiter = conf['delimiter']
        except Exception as err:
            print(err)
    firstset = True
    print("Exporting as CSV")
    print(len(data))
    print(outfile)
    with open(outfile, "a") as file:
        file.truncate(0)
        w = csv.writer(file, delimiter=delimiter)
        for x in data:
            if firstset:
                w.writerow(x.keys())
                firstset = False
            arr = []
            for y in x.values():
                arr.append(y['value'])
            print("Exporting line " + json.dumps(arr))
            w.writerow(arr)


def exportcsvfromfile(source, outfile):
    """
    Exports the given data, which should be a list of dictionaries (expect errors if it isn't one)
    as a CSV file. First row includes the column names, all others include values
    :param source: json file created by import
    :param outfile: location of the file
    :return:
    """
    delimiter = ';'
    with open('../resources/outconfig.json') as file:
        try:
            conf = json.loads(file.read())
            delimiter = conf['delimiter']
        except Exception as err:
            print(err)
    firstset = True
    print("Exporting as CSV")
    with open(source, 'r') as sauce:
        with open(outfile, "a") as file:
            file.truncate(0)
            w = csv.writer(file, delimiter=delimiter)
            sauce.readline()
            try:
                while True:
                    x = util.parseline(sauce.readline())
                    if firstset:
                        w.writerow(x.keys())
                        firstset = False
                    arr = []
                    for y in x.values():
                        arr.append(y['value'])
                    print("Exporting line " + json.dumps(arr))
                    w.writerow(arr)
            except Exception as err:
                print(err)
