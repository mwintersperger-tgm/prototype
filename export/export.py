import json
import csv
import ast
from pandas import DataFrame


class ExportCls(object):
    @staticmethod
    def fetch(dataset):
        # TODO: receive data to export
        pass

    @staticmethod
    def exportExcel(data):
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
        frame.to_excel("../resources/data/test.xlsx", sheet_name="test", index=False)

def test():
    tmp = [];
    inc = 0;
    with open("../resources/data/data.json","r") as file:
        for x in range(0, 1000):
            try:
                y = file.readline()
                print(y)
                tmp.append(json.loads(y))
                inc+=1
                print(str(inc) + " lines read")
            except Exception as err:
                print(err)
    print("File to export:\n" + str(tmp))
    ExportCls.exportExcel(tmp)


if __name__ == '__main__':
    test()
    pass
