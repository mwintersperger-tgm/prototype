import csv
import json
from builtins import staticmethod

class ImportCls(object):
    @staticmethod
    def forward(dataset):
        print("putting out output")
        with open("data.json", "a") as outfile:
            try:
                print("writing now")
                outfile.write(json.dumps(dataset) + "\n")
                outfile.close()
            except Exception as err:
                print(str(err))
        pass

    @staticmethod
    def importcsv():
        cfg = {}
        with open("inconfig.json") as file:
            cfg = json.load(file)
        if isinstance(cfg['delimiter'], int):
            cfg['delimiter'] = chr(cfg['delimiter'])
        with open(cfg['file']) as file:
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
            print(str(count) + " lines imported")


if __name__ == '__main__':
    ImportCls.importcsv()
