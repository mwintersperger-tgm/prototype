import json
import csv
from random import randint
true = True
false = False


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


def lel(argsin):
    try:
        ret = argsin['return']
    except KeyError:
        ret = False
    with open("../resources/param.json") as file:
        columns = json.load(file)
    result = []
    ccsv = columns['createcsv']
    try:
        if argsin['writecsv']:
            ccsv = True
    except KeyError:
        pass
    cjson = columns['createjson']
    try:
        if argsin['writejson']:
            cjson = True
    except KeyError:
        pass
    delim = columns['delimiter']
    try:
        if isinstance(delim, int):
            delim = chr(delim)
    except KeyError:
        pass
    try:
        jsonloc = argsin['jsonname']
    except KeyError:
        pass
    try:
        csvloc = argsin['csvname']
    except KeyError:
        pass
    try:
        if argsin['lines'] > 0:
            lines = argsin['lines']
    except KeyError:
        lines = columns['lines']
    try:
        param = argsin['param']
    except KeyError:
        param = columns['param']
    if ccsv:
        with open(csvloc, "a") as csvfile:
            w = None
            if ccsv:
                csvfile.truncate(0)
                w = csv.writer(csvfile, delimiter=delim)
            linecount = 0
            for i in range(0, lines):
                newres = {}
                for x in param:
                    newres[x['propname']] = generate(x['generator'])
                    pass
                # result.append(newres)
                if linecount == 0:
                    if ccsv:
                        w.writerow(newres.keys())
                if ccsv:
                    w.writerow(newres.values())
                if cjson or ret:
                    result.append(newres)
                linecount += 1
    else:
        for i in range(0, lines):
            newres = {}
            for x in param:
                newres[x['propname']] = generate(x['generator'])
                pass
            # result.append(newres)
            if cjson or ret:
                result.append(newres)

    if cjson:
        with open(jsonloc, "w") as file:
            file.truncate(0)
            file.write(json.dumps(result))

    if ret:
        return result

