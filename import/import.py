import csv
import json
import os
from builtins import staticmethod



class ImportCls(object):
    @staticmethod
    def forward(dataset):
        with open("../resources/data/data.json", "a") as outfile:
            try:
                outfile.write(json.dumps(dataset) + ",\n")
                outfile.close()
                print(json.dumps(dataset))
            except Exception as err:
                print(str(err))
        pass

    @staticmethod
    def startFile():
        with open("../resources/data/data.json", "w") as outfile:
            outfile.truncate(0)
            outfile.write('{"rules":"", "values":[\n')

    @staticmethod
    def endFile():
        with open("../resources/data/data.json", "a") as outfile:
            outfile.truncate(os.path.getsize("../resources/data/data.json") - 3)
            outfile.write('\n]}')

    @staticmethod
    def importcsv():
        cfg = {}
        with open("../resources/inconfig.json") as file:
            cfg = json.load(file)
        if isinstance(cfg['delimiter'], int):
            cfg['delimiter'] = chr(cfg['delimiter'])
        with open(cfg['file']) as file:
            ImportCls.startFile()
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
                        ImportCls.forward(res)
                        count+=1
            ImportCls.endFile()
            print(str(count) + " lines imported")


if __name__ == '__main__':
    ImportCls.importcsv()
