import json
import csv
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
    def exportCSV(data, filename):
        """
        Exports the given data, which should be a list of dictionaries (expect errors if it isn't one)
        as a CSV file. First row includes the column names, all others include values
        :param data: list of dicts
        :param filename: location of the file
        :return:
        """
        firstset = True
        print("Exporting as CSV")
        print(len(data))
        print(filename)
        with open(filename, "a") as file:
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
