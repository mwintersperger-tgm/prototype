import json
import os


def keysonly(obj, keyset):
    """
    returns an object that uses values from the input object that are relevant to the keyset.
    If a keyset attribute doesn't exist, None is used instead. This function should never throw errors, therefore this
    failsafe is built into it.
    For example object = {"name":"alex", "age":19} and keyset = ["name"] would return {"name":"alex"}
    :param obj:
    :param keyset:
    :return:
    """
    out = dict()
    for x in keyset:
        try:
            out[x] = obj[x]
        except Exception:
            out[x] = None
    return out


def keyalign(object1, object2, keyset):
    """
    checks if the keysets of the two given objects are the same
    :param object1:
    :param object2:
    :param keyset:
    :return:
    """
    try:
        for x in keyset:
            if object1[x] != object2[x]:
                return False
        return True
    except Exception as err:
        print(err)
        return False


def mergeline(objects, keyset):
    """
    merges dicts in the objects list into one dataset if the values in the keyset align.
    :param objects: list of input objects
    :param keyset: keys to determine which attributes have to align for a successful merge
    :return: merge result
    """

    try:
        outdict = objects[0]
        if not isinstance(outdict, dict):
            return None
        objects.remove(objects[0])
        print("first object")
        print(outdict)
        for x in objects:
            if isinstance(x, dict):
                print("Key Alignment: ", keyalign(outdict, x, keyset))
                if keyalign(outdict, x, keyset):
                    for y in x.keys():
                        if y not in outdict.keys():
                            outdict[y] = x[y]
        return outdict
    except Exception as err:
        print(err)
        return {}


def mergelinerisky(objects):
    """
    doesn't check for keyset alignment, only checks if the attribute already exists in the dict.
    As a result, using this method is more risky, but better in terms of performance if you already made sure that the
    keysets of all objects align (by means of groupbykeys or something).
    :param objects:
    :return:
    """
    try:
        outdict = {}
        for x in objects:
            if isinstance(x, dict):
                for y in x.keys():
                    if y not in outdict.keys():
                        outdict[y] = x[y]
        return outdict
    except Exception as err:
        print(err)
        return {}


def gatherkeys(objects, keyset):
    """
    collects all available combinations of keys and adds them into a list
    :param objects: list
    :param keyset: list
    :return:
    """

    array = []
    for obj in objects:
        orig = True
        # expected behavior: keys are not allowed to be null / None
        for x in keyset:
            if x not in obj.keys():
                orig = False

        if orig:
            for key in array:
                if keyalign(obj, key, keyset):
                    orig = False
        if orig:
            array.append(keysonly(obj, keyset))
    return array


def gatherkeysallownone(objects, keyset):
    """
    collects all available combinations of keys and adds them into a list.
    Allows for keys that are not set to be added as None values
    :param objects: list
    :param keyset: list
    :return:
    """

    array = []
    for obj in objects:
        orig = True
        for key in array:
            if keyalign(obj, key, keyset):
                orig = False
        if orig:
            array.append(keysonly(obj, keyset))
    return array


def getkeygroup(objects, keyset):
    """
    returns a list filled with all objects with the given keyset.
    :param objects: list
    :param keyset: dict
    :return:
    """
    array = []
    for x in objects:
        if keyalign(x, keyset, keyset.keys()):
            array.append(x)

    return array


def groupbykeys(objects, keysets):
    """
    creates a json structure:
    [
        {
            "key": {},
            "values": [
                {}
            ]
        }
    ]
    by grouping the given objects into arrays ("values") based on the keysets they align with.
    There is one "key", "values" entry for each of the given keysets.
    Both objects and keysets are expected to be arrays of dictionaries (if they aren't, expect errors).
    :param objects:
    :param keysets:
    :return:
    """

    array = []
    for x in keysets:
        tmp = dict()
        tmp['key'] = x
        tmp['values'] = []
        array.append(tmp)

    for x in objects:
        for y in array:
            if keyalign(x, y['key'], y['key'].keys()):
                y['values'].append(x)

    return array


def finalmerge(gbkobjects):
    """
    expects the output from groupbykeys as a parameter to initiate the final merge.
    made obsolete by the less memory consuming getkeygroup + mergelinerisky
    method used in finalmerge since gbk may eats too much memory
    :param gbkobjects:
    :return:
    """
    array = []
    for x in gbkobjects:
        array.append(mergelinerisky(x['values']))
    return array


def fullmerge(objects, keyset):
    tmp = gatherkeys(objects, keyset)
    out = []
    for x in tmp:
        tmp2 = getkeygroup(objects, x)
        out.append(mergelinerisky(tmp2))
    return out


def memconservingmerge(filepaths, keyset, outfile):
    key = list()
    for filepath in filepaths:
        with open(filepath, "r") as file:
            file.readline()
            try:
                while True:
                    s = file.readline()
                    if s[len(s) - 2] == ',':
                        obj = json.loads(s[:-2])
                    else:
                        obj = json.loads(s)
                    for x in obj.keys():
                        obj[x] = obj[x]['value']
                    obj2 = keysonly(obj, keyset)
                    if obj2 not in key:
                        key.append(obj2)
            except Exception as err:
                print(err)
                pass
    print('Final Keys: ' + str(key) + '; length: ' + str(len(key)))
    with open(outfile, "a") as file:
        file.write('{"rules":"", "values":[\n')
    for k in key:
        tempobj = k
        for filepath in filepaths:
            with open(filepath, "r") as file:
                file.readline()
                try:
                    while True:
                        s = file.readline()
                        if s[len(s) - 2] == ',':
                            obj = json.loads(s[:-2])
                        else:
                            obj = json.loads(s)
                        for x in obj.keys():
                            obj[x] = obj[x]['value']
                        if keyalign(k, obj, keyset):
                            tempobj = mergelinerisky([tempobj, obj])
                except Exception as err:
                    pass
        print('outobj: ' + str(tempobj))
        try:
            with open(outfile, "a") as file:
                file.write(json.dumps(tempobj)+',\n')
        except Exception as err:
            pass
    with open(outfile, "a") as file:
        file.truncate(os.path.getsize(outfile) - 3)
        file.write('\n]}')

