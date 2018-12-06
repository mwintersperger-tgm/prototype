import json
import csv
import os
import argparse
from random import randint
true = True
false = False

parser = argparse.ArgumentParser()

parser.add_argument("-json", "--writejson", help="use this option to generate a JSON file in resources/data", action='store_true')

parser.add_argument("-csv", "--writecsv", help="use this option to generate a CSV file in resources/data", action='store_true')

parser.add_argument("-l", "--lines",
                    help="Sets the amount of lines generated",
                    type=int, required=False, default=-1, nargs='?', const=True)

parser.add_argument("-csvn", "--csvname",
                    help="Sets the name and location of the generated csv file",
                    type=str, required=False, default="../resources/data/result.csv", nargs='?', const=True)

parser.add_argument("-jsonn", "--jsonname",
                    help="Sets the name and location of the generated json file",
                    type=str, required=False, default="../resources/data/result.csv", nargs='?', const=True)

args = parser.parse_args()


def generate(generator):
    """
    Generates a value based on the given generator, which has to be a string
    Read the generate_readme for further information
    :param generator: string
    :return:
    """
    if generator.startswith("name"):
        stri = ""
        stri += chr(randint(65, 90))
        for xa in range(0, randint(5, 11)):
            stri += chr(randint(97, 122))
        return stri
    elif generator.startswith("randchar"):
        stri = ""
        for xb in range(0, int(generator[8:])):
            num = randint(0, 2)
            if num == 2:
                stri += chr(randint(48, 57))
            elif num == 1:
                stri += chr(randint(65, 90))
            else:
                stri += chr(randint(95, 122))

        return stri
    elif generator.startswith("randint"):
        stri = "1"
        for xc in range(0, int(generator[7:])):
            stri += "0"
        return randint(0, int(stri) - 1)
    else:
        return "hi"


if __name__ == '__main__':
    colums = {}
    with open("../resources/param.json") as file:
        columns = json.load(file)
    print(json.dumps(columns))
    result = []
    ccsv = columns['createcsv']
    if args.writecsv:
        ccsv = True
    cjson = columns['createjson']
    if args.writejson:
        cjson = True
    delim = columns['delimiter']
    if isinstance(delim, int):
        delim = chr(delim)
    delete = false
    jsonloc = args.jsonname
    csvloc = args.csvname
    lines = columns['lines']
    if args.lines > 0:
        lines = args.lines
    with open(csvloc, "a") as csvfile:
        w = None
        if ccsv:
            csvfile.truncate(0)
            w = csv.writer(csvfile, delimiter=delim)
        linecount = 0
        for i in range(0, lines):
            newres = {}
            for x in columns['param']:
                newres[x['propname']] = generate(x['generator'])
                pass
            # result.append(newres)
            if linecount == 0:
                if ccsv:
                    w.writerow(newres.keys())
            print(newres)
            print("linecount: " + str(linecount+1))
            if ccsv:
                w.writerow(newres.values())
            if cjson:
                result.append(newres)
            linecount += 1

    if not ccsv:
        if os.stat(csvloc).st_size <= 0:
            os.remove(csvloc)

    # print(json.dumps(result))
    if cjson:
        with open(jsonloc, "w") as file:
            file.truncate(0)
            file.write(json.dumps(result))
