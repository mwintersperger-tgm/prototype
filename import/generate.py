import json
import csv
from random import randint
true = True
false = False
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-json", "--writejson", help="use this option to generate a JSON file in resources/data",action='store_true')

parser.add_argument("-csv", "--writecsv", help="use this option to generate a CSV file in resources/data",action='store_true')

args = parser.parse_args()


def generate(generator):
    """
    Generates a value based on the given generator, which has to be a string
    Read the generate_readme for further information
    :param generator: string
    :return:
    """
    if generator.startswith("name"):
        str = ""
        str += chr(randint(65, 90))
        for x in range(0, randint(5,11)):
            str += chr(randint(97, 122))
        return str
    elif generator.startswith("randchar"):
        str = ""
        for x in range(0,int(generator[8:])):
            str += chr(randint(48,122))
        return str
    elif generator.startswith("randint"):
        str = "1"
        for x in range(0,int(generator[7:])):
            str += "0"
        return randint(0,int(str) - 1)
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
    with open("../resources/data/result.csv", "w") as csvfile:
        if ccsv:
            csvfile.truncate(0)
            w = csv.writer(csvfile, delimiter=delim)
        linecount = 0
        for i in range(0,columns['lines']):
            newres = {}
            for x in columns['param']:
                newres[x['propname']] = generate(x['generator'])
                pass
            # result.append(newres)
            if linecount == 0:
                w.writerow(newres.keys())
            print(newres)
            print("linecount: " + str(linecount+1))
            if ccsv:
                w.writerow(newres.values())
            if cjson:
                result.append(newres)
            linecount += 1

        # print(json.dumps(result))
    if cjson:
        with open("../resources/data/result.json","w") as file:
            file.truncate(0)
            file.write(json.dumps(result))
