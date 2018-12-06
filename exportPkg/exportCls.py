import json
import csv
import ast
from pandas import DataFrame


class ExportCls(object):
    @staticmethod
    def fetch(dataset):
        """
        I don't know where this is going or how I plan to receive data
        :param dataset:
        :return:
        """
        # TODO: receive data to export
        pass

    @staticmethod
    def exportExcel(data):
        """
        Exports the given data, which should be a list of dictionaries (expect errors if it isn't one)
        as an excel file. The first row will feature the row names as bold text, all other rows will
        be filled with the data received from one of the dicts in the list.
        :param data: list of dicts
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
        frame.to_excel("../resources/data/test.xlsx", sheet_name="test", index=False)

    @staticmethod
    def exportCSV(data):
        """
        Exports the given data, which should be a list of dictionaries (expect errors if it isn't one)
        as a CSV file. First row includes the column names, all others include values
        :param data: list of dicts
        :return:
        """
        firstset = True
        print("Exporting as CSV")
        print(len(data))
        with open("../resources/data/test.csv", "a") as file:
            file.truncate(0)
            w = csv.writer(file, delimiter="|")
            for x in data:
                if firstset:
                    w.writerow(x.keys())
                    firstset = False
                arr = []
                for y in x.values():
                    arr.append(y['value'])
                print("Exporting line " + json.dumps(arr))
                w.writerow(arr)


def test():
    """
    Tests the functionality of exportExcel()
    :return:
    """
    tmp = [];
    inc = 0;
    with open("../resources/data/data.json", "r") as file:
        for x in range(0, 1001):
            try:
                y = file.readline()
                print("'" + y[len(y) - 2:len(y) - 1] + "' == '" + ",'")
                if y[len(y) - 2:len(y) - 1] == ",":
                    y = y[:len(y)-2]
                tmp.append(json.loads(y))
                inc+=1
                print(str(inc) + " lines read")
            except Exception as err:
                print(err)
    print("File to export:\n" + str(tmp))
    print("Length of file to export:" + str(len(tmp)))
    ExportCls.exportExcel(tmp)
    ExportCls.exportCSV(tmp)


if __name__ == '__main__':
    # runs test(). May be removed later
    test()
    pass
