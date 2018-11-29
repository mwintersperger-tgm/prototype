import csv
import json
import os
import argparse
from builtins import staticmethod

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--delimiter",
					help="Sets the delimiter used for importing the CSV file",
                    type=str, required=False, default="", nargs='?', const=True)

parser.add_argument("-file", "--fileinput",
					help="Sets the location of the file that should be imported",
                    type=str, required=False, default="", nargs='?', const=True)

parser.add_argument("-out", "--fileoutput",
					help="Sets the location, the converted JSON file will be saved at",
                    type=str, required=False, default="", nargs='?', const=True)

args = parser.parse_args()

class ImportCls(object):
    @staticmethod
    def forward(dataset, file):
        with open(file, "a") as outfile:
            try:
                outfile.write(json.dumps(dataset) + ",\n")
                outfile.close()
                print(json.dumps(dataset))
            except Exception as err:
                print(str(err))
        pass

    @staticmethod
    def startFile(file):
        with open(file, "w") as outfile:
            outfile.truncate(0)
            outfile.write('{"rules":"", "values":[\n')

    @staticmethod
    def endFile(file):
        with open(file, "a") as outfile:
            outfile.truncate(os.path.getsize("../resources/data/data.json") - 3)
            outfile.write('\n]}')

    @staticmethod
    def importcsv(args):
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
            ImportCls.startFile(cfg['out'])
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
                        for x in range(0,len(temp)):
                            res[colnames[0][x]] = {}
                            res[colnames[0][x]]["value"] = temp[x]
                            res[colnames[0][x]]["validated"] = False
                        ImportCls.forward(res, cfg['out'])
                        count+=1
            ImportCls.endFile(cfg['out'])
            print(str(count) + " lines imported")


if __name__ == '__main__':
    ImportCls.importcsv(args)
