import json
import csv


class ExportCls(object):
    @staticmethod
    def fetch(dataset):
        # TODO: receive data to export
        pass

    @staticmethod
    def exportCsv():
        cfg = {}
        with open("outconfig.json") as file:
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
    pass
