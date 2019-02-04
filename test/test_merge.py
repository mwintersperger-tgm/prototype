import json
import exportPkg.merge as merge
import pytest
import os
import shutil
import importPkg.generate as generateFile
import copy

@pytest.fixture()
def testobj():
    obj = list()
    obj.append(json.loads('{"fname":"a", "lname":"b", "uid":"hello"}'))
    obj.append(json.loads('{"fname":"a", "lname":"b", "age":27}'))
    obj.append(json.loads('{"fname":"a", "lname":"b", "gid":"world"}'))
    obj.append(json.loads('{"fname":"a", "lname":"c", "uid":"hi"}'))
    obj.append(json.loads('{"fname":"a", "lname":"c", "age":22}'))
    obj.append(json.loads('{"fname":"d", "lname":"e", "uid":"soup"}'))
    obj.append(json.loads('{"fname":"d", "lname":"e", "gid":"liquid"}'))
    obj.append(json.loads('{"fname":"f", "lname":"e", "age":19}'))
    print('testobj: ', obj)
    yield obj


@pytest.fixture()
def keys():
    keys = json.loads('["fname", "lname"]')
    print('keys: ', keys)
    yield keys


@pytest.fixture()
def keysets(keys, testobj):
    ks = merge.gatherkeys(testobj, keys)
    print('keysets: ', ks)
    yield ks


def testkeysonly(testobj, keys):
    res = str(merge.keysonly(testobj[0], keys))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'b'}"


def testkeysonlymissingvalue(keys):
    obj = dict()
    obj['fname'] = "z"
    res = str(merge.keysonly(obj, keys))
    print(obj)
    print(res)
    assert res == "{'fname': 'z', 'lname': None}"


def testkeyalign(testobj, keys):
    assert merge.keyalign(testobj[0], testobj[1], keys)


def testkeyalignfailed(testobj, keys):
    assert not merge.keyalign(testobj[0], testobj[4], keys)


def testkeyalignnokey(testobj, keys):
    other = dict()
    other["fname"] = "z"
    assert merge.keyalign(testobj[0], other, keys) == False


def testmergeline(testobj, keys):
    tmp = list()
    tmp.append(testobj[0])
    tmp.append(testobj[1])
    res = str(merge.mergeline(tmp, keys))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'b', 'uid': 'hello', 'age': 27}"


def testmergelinefailed(testobj, keys):
    tmp = list()
    tmp.append(testobj[0])
    tmp.append(testobj[4])
    res = str(merge.mergeline(tmp, keys))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'b', 'uid': 'hello'}"


def testmergelinefailedmirror(testobj, keys):
    tmp = list()
    tmp.append(testobj[4])
    tmp.append(testobj[0])
    res = str(merge.mergeline(tmp, keys))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'c', 'age': 22}"


def testmergelineonedict(testobj, keys):
    tmp = list()
    tmp.append(testobj[0])
    tmp.append(12)
    res = str(merge.mergeline(tmp, keys))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'b', 'uid': 'hello'}"


def testmergelineonedictmirror(testobj, keys):
    tmp = list()
    tmp.append(12)
    tmp.append(testobj[0])
    res = merge.mergeline(tmp, keys)
    print(res)
    assert res is None


def testmergelinenodict(keys):
    tmp = list()
    tmp.append(12)
    tmp.append("Helloworld")
    res = merge.mergeline(tmp, keys)
    print(res)
    assert res is None


def testmergelinerisky(testobj):
    tmp = list()
    tmp.append(testobj[0])
    tmp.append(testobj[1])
    res = str(merge.mergelinerisky(tmp))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'b', 'uid': 'hello', 'age': 27}"


def testmergelineriskymismatch(testobj):
    tmp = list()
    tmp.append(testobj[0])
    tmp.append(testobj[4])
    res = str(merge.mergelinerisky(tmp))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'b', 'uid': 'hello', 'age': 22}"


def testmergelineriskymismatchmirror(testobj):
    tmp = list()
    tmp.append(testobj[4])
    tmp.append(testobj[0])
    res = str(merge.mergelinerisky(tmp))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'c', 'age': 22, 'uid': 'hello'}"


def testmergelineriskyonedict(testobj):
    tmp = list()
    tmp.append(testobj[0])
    tmp.append(12)
    res = str(merge.mergelinerisky(tmp))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'b', 'uid': 'hello'}"


def testmergelineriskyonedictmirror(testobj):
    tmp = list()
    tmp.append(12)
    tmp.append(testobj[0])
    res = str(merge.mergelinerisky(tmp))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'b', 'uid': 'hello'}"


def testmergelineriskynodict():
    tmp = list()
    tmp.append(12)
    tmp.append("Helloworld")
    res = str(merge.mergelinerisky(tmp))
    print(res)
    assert res == "{}"


def testgatherkeys(testobj, keys):
    res = str(merge.gatherkeys(testobj, keys))
    print(res)
    assert res == "[{'fname': 'a', 'lname': 'b'}, {'fname': 'a', 'lname': 'c'}, {'fname': 'd', 'lname': 'e'}, {'fname': 'f', 'lname': 'e'}]"


def testgatherkeyswrongentry(testobj, keys):
    testobj.append(json.loads('{"fname": "x", "uid": "y"}'))
    res = str(merge.gatherkeys(testobj, keys))
    print(res)
    assert res == "[{'fname': 'a', 'lname': 'b'}, {'fname': 'a', 'lname': 'c'}, {'fname': 'd', 'lname': 'e'}, {'fname': 'f', 'lname': 'e'}]"


def testgatherkeysempty(keys):
    res = str(merge.gatherkeys([], keys))
    print(res)
    assert res == "[]"


def testgatherkeysnone(testobj, keys):
    res = str(merge.gatherkeysallownone(testobj, keys))
    print(res)
    assert res == "[{'fname': 'a', 'lname': 'b'}, {'fname': 'a', 'lname': 'c'}, {'fname': 'd', 'lname': 'e'}, {'fname': 'f', 'lname': 'e'}]"


def testgatherkeysnonewrongentry(testobj, keys):
    testobj.append(json.loads('{"fname": "x", "uid": "y"}'))
    res = str(merge.gatherkeysallownone(testobj, keys))
    print(res)
    assert res == "[{'fname': 'a', 'lname': 'b'}, {'fname': 'a', 'lname': 'c'}, {'fname': 'd', 'lname': 'e'}, {'fname': 'f', 'lname': 'e'}, {'fname': 'x', 'lname': None}]"


def testgatherkeysnoneempty(keys):
    res = str(merge.gatherkeysallownone([], keys))
    print(res)
    assert res == "[]"


def testkeygroup(testobj, keysets):
    res = str(merge.getkeygroup(testobj, keysets[0]))
    print(res)
    assert res == "[{'fname': 'a', 'lname': 'b', 'uid': 'hello'}, {'fname': 'a', 'lname': 'b', 'age': 27}, {'fname': 'a', 'lname': 'b', 'gid': 'world'}]"


def testkeygroupemptyobject(keysets):
    res = str(merge.getkeygroup([], keysets[0]))
    print(res)
    assert res == "[]"


def testkeygroupemptykeyset(testobj):
    res = str(merge.getkeygroup(testobj, {}))
    print(res)
    assert res == str(testobj)


def testgroupkeys(testobj, keysets):
    res = str(merge.groupbykeys(testobj, keysets))
    print(res)
    assert res == "[{'key': {'fname': 'a', 'lname': 'b'}, 'values': [{'fname': 'a', 'lname': 'b', 'uid': 'hello'}, {'fname': 'a', 'lname': 'b', 'age': 27}, {'fname': 'a', 'lname': 'b', 'gid': 'world'}]}, {'key': {'fname': 'a', 'lname': 'c'}, 'values': [{'fname': 'a', 'lname': 'c', 'uid': 'hi'}, {'fname': 'a', 'lname': 'c', 'age': 22}]}, {'key': {'fname': 'd', 'lname': 'e'}, 'values': [{'fname': 'd', 'lname': 'e', 'uid': 'soup'}, {'fname': 'd', 'lname': 'e', 'gid': 'liquid'}]}, {'key': {'fname': 'f', 'lname': 'e'}, 'values': [{'fname': 'f', 'lname': 'e', 'age': 19}]}]"


def testgroupkeysnoobjects(testobj, keysets):
    res = str(merge.groupbykeys([], keysets))
    print(res)
    assert res == "[{'key': {'fname': 'a', 'lname': 'b'}, 'values': []}, {'key': {'fname': 'a', 'lname': 'c'}, 'values': []}, {'key': {'fname': 'd', 'lname': 'e'}, 'values': []}, {'key': {'fname': 'f', 'lname': 'e'}, 'values': []}]"


def testgroupkeysnokeysets(testobj):
    res = str(merge.groupbykeys(testobj, []))
    print(res)
    assert res == "[]"


def testgroupkeysemptykeyset(testobj):
    res = str(merge.groupbykeys(testobj, json.loads('[{}]')))
    print(res)
    assert res == "[{'key': {}, 'values': " + str(testobj) + "}]"


def testfinalmerge(testobj, keysets):
    res = str(merge.finalmerge(merge.groupbykeys(testobj, keysets)))
    print(res)
    assert res == "[{'fname': 'a', 'lname': 'b', 'uid': 'hello', 'age': 27, 'gid': 'world'}, {'fname': 'a', 'lname': 'c', 'uid': 'hi', 'age': 22}, {'fname': 'd', 'lname': 'e', 'uid': 'soup', 'gid': 'liquid'}, {'fname': 'f', 'lname': 'e', 'age': 19}]"


def testfullmerge(testobj, keys):
    res = str(merge.fullmerge(testobj, keys))
    print(res)
    assert res == "[{'fname': 'a', 'lname': 'b', 'uid': 'hello', 'age': 27, 'gid': 'world'}, {'fname': 'a', 'lname': 'c', 'uid': 'hi', 'age': 22}, {'fname': 'd', 'lname': 'e', 'uid': 'soup', 'gid': 'liquid'}, {'fname': 'f', 'lname': 'e', 'age': 19}]"


def testmemconservingmerge():
    os.makedirs(os.path.dirname(os.path.abspath(__file__)) + "\\tmp")
    args = dict()
    args['param'] = json.loads('[{"propname":"firstname","generator":"name"},{"propname":"lastname","generator":"name"},{"propname":"bla","generator":"randchar8"},{"propname":"wtf","generator":"randchar8"},{"propname":"wtf2","generator":"randint8"},{"propname":"wtf3","generator":"randint6"}]')
    args['lines'] = 10
    args['return'] = True
    tmp = generateFile.lel(args)
    with open('tmp/data1.jayson', "a") as file:
        file.write(',\n')
    with open('tmp/data2.jayson', "a") as file:
        file.write(',\n')
    for y in tmp:
        obj1 = merge.keysonly(y, ['firstname', 'lastname', 'bla', 'wtf'])
        for x in obj1.keys():
            tmp1 = obj1[x]
            obj1[x] = dict()
            obj1[x]['value'] = tmp1
        obj2 = merge.keysonly(y, ['firstname', 'lastname', 'wtf2', 'wtf3'])
        for x in obj2.keys():
            tmp1 = obj2[x]
            obj2[x] = dict()
            obj2[x]['value'] = tmp1
        with open('tmp/data1.jayson', "a") as file:
            file.write(json.dumps(obj1) + ',\n')
        with open('tmp/data2.jayson', "a") as file:
            file.write(json.dumps(obj2) + ',\n')
    open('tmp/data.jayson', "a").close()
    merge.memconservingmerge(['tmp/data1.jayson', 'tmp/data2.jayson'], ['firstname', 'lastname'], 'tmp/data.jayson')
    res = list()
    with open('tmp/data.jayson', "r") as file:
        file.readline()
        try:
            while True:
                s = file.readline()
                if s[len(s) - 2] == ',':
                    obj = json.loads(s[:-2])
                else:
                    obj = json.loads(s)
                res.append(obj)
        except Exception as err:
            print('test 299: ' + str(err))
    print('length: ' + str(len(res)) + '; result list: ' + str(res) )
    print('length: ' + str(len(tmp)) + '; source list: ' + str(tmp))
    exists = True
    for x in tmp:
        if x not in res:
            exists = False
    shutil.rmtree(os.path.dirname(os.path.abspath(__file__)) + "\\tmp")
    assert exists
