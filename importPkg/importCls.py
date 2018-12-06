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


def end_file(file):
    with open(file, "a") as outfile:
        outfile.truncate(os.path.getsize("../resources/data/data.json") - 3)
        outfile.write('\n]}')


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
        ImportCls.start_file(cfg['out'])
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
                    ImportCls.forward(res, cfg['out'])
                    count += 1
        ImportCls.end_file(cfg['out'])
        print(str(count) + " lines imported")
