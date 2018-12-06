from exportPkg.exportCls import ExportCls
import json


def test():
    """
    Tests the functionality of exportExcel()
    :return:
    """
    tmp = []
    inc = 0
    with open("../resources/data/data.json", "r") as file:
        for x in range(0, 1001):
            try:
                y = file.readline()
                print("'" + y[len(y) - 2:len(y) - 1] + "' == '" + ",'")
                if y[len(y) - 2:len(y) - 1] == ",":
                    y = y[:len(y)-2]
                tmp.append(json.loads(y))
                inc += 1
                print(str(inc) + " lines read")
            except Exception as err:
                print(err)
    print("File to export:\n" + str(tmp))
    print("Length of file to export:" + str(len(tmp)))
    ExportCls.exportExcel(tmp)
    ExportCls.exportCSV(tmp, "../resources/data/test.csv")


if __name__ == '__main__':
    # runs test(). May be removed later
    test()
    pass