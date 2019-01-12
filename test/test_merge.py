import json
import exportPkg.merge as Merge
import pytest


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
    ks = Merge.gatherkeys(testobj, keys)
    print('keysets: ', ks)
    yield ks


def testfullmerge(testobj, keys):
    res = str(Merge.fullmerge(testobj, keys))
    print(res)
    assert res == "[{'fname': 'a', 'lname': 'b', 'uid': 'hello', 'age': 27, 'gid': 'world'}, {'fname': 'a', 'lname': 'c', 'uid': 'hi', 'age': 22}, {'fname': 'd', 'lname': 'e', 'uid': 'soup', 'gid': 'liquid'}, {'fname': 'f', 'lname': 'e', 'age': 19}]"


def testgroupkeys(testobj, keysets):
    res = str(Merge.groupbykeys(testobj, keysets))
    print(res)
    assert False


