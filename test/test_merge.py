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


def testkeysonly(testobj, keys):
    res = str(Merge.keysonly(testobj[0], keys))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'b'}"


def testkeysonlymissingvalue(keys):
    obj = dict()
    obj['fname'] = "z"
    res = str(Merge.keysonly(obj, keys))
    print(obj)
    print(res)
    assert res == "{'fname': 'z', 'lname': None}"


def testkeyalign(testobj, keys):
    assert Merge.keyalign(testobj[0], testobj[1], keys)


def testkeyalignfailed(testobj, keys):
    assert not Merge.keyalign(testobj[0], testobj[4], keys)


def testkeyalignnokey(testobj, keys):
    other = dict()
    other["fname"] = "z"
    assert Merge.keyalign(testobj[0], other, keys) == False


def testmergeline(testobj, keys):
    tmp = list()
    tmp.append(testobj[0])
    tmp.append(testobj[1])
    res = str(Merge.mergeline(tmp, keys))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'b', 'uid': 'hello', 'age': 27}"


def testmergelinefailed(testobj, keys):
    tmp = list()
    tmp.append(testobj[0])
    tmp.append(testobj[4])
    res = str(Merge.mergeline(tmp, keys))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'b', 'uid': 'hello'}"


def testmergelinefailedmirror(testobj, keys):
    tmp = list()
    tmp.append(testobj[4])
    tmp.append(testobj[0])
    res = str(Merge.mergeline(tmp, keys))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'c', 'age': 22}"


def testmergelineonedict(testobj, keys):
    tmp = list()
    tmp.append(testobj[0])
    tmp.append(12)
    res = str(Merge.mergeline(tmp, keys))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'b', 'uid': 'hello'}"


def testmergelineonedictmirror(testobj, keys):
    tmp = list()
    tmp.append(12)
    tmp.append(testobj[0])
    res = Merge.mergeline(tmp, keys)
    print(res)
    assert res is None


def testmergelinenodict(keys):
    tmp = list()
    tmp.append(12)
    tmp.append("Helloworld")
    res = Merge.mergeline(tmp, keys)
    print(res)
    assert res is None


def testmergelinerisky(testobj):
    tmp = list()
    tmp.append(testobj[0])
    tmp.append(testobj[1])
    res = str(Merge.mergelinerisky(tmp))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'b', 'uid': 'hello', 'age': 27}"


def testmergelineriskymismatch(testobj):
    tmp = list()
    tmp.append(testobj[0])
    tmp.append(testobj[4])
    res = str(Merge.mergelinerisky(tmp))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'b', 'uid': 'hello', 'age': 22}"


def testmergelineriskymismatchmirror(testobj):
    tmp = list()
    tmp.append(testobj[4])
    tmp.append(testobj[0])
    res = str(Merge.mergelinerisky(tmp))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'c', 'age': 22, 'uid': 'hello'}"


def testmergelineriskyonedict(testobj):
    tmp = list()
    tmp.append(testobj[0])
    tmp.append(12)
    res = str(Merge.mergelinerisky(tmp))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'b', 'uid': 'hello'}"


def testmergelineriskyonedictmirror(testobj):
    tmp = list()
    tmp.append(12)
    tmp.append(testobj[0])
    res = str(Merge.mergelinerisky(tmp))
    print(res)
    assert res == "{'fname': 'a', 'lname': 'b', 'uid': 'hello'}"


def testmergelineriskynodict():
    tmp = list()
    tmp.append(12)
    tmp.append("Helloworld")
    res = str(Merge.mergelinerisky(tmp))
    print(res)
    assert res == "{}"


def testkeysets(testobj, keys):
    res = str(Merge.gatherkeys(testobj, keys))
    print(res)
    assert res == "[{'fname': 'a', 'lname': 'b'}, {'fname': 'a', 'lname': 'c'}, {'fname': 'd', 'lname': 'e'}, {'fname': 'f', 'lname': 'e'}]"


def testfullmerge(testobj, keys):
    res = str(Merge.fullmerge(testobj, keys))
    print(res)
    assert res == "[{'fname': 'a', 'lname': 'b', 'uid': 'hello', 'age': 27, 'gid': 'world'}, {'fname': 'a', 'lname': 'c', 'uid': 'hi', 'age': 22}, {'fname': 'd', 'lname': 'e', 'uid': 'soup', 'gid': 'liquid'}, {'fname': 'f', 'lname': 'e', 'age': 19}]"


def testgroupkeys(testobj, keysets):
    res = str(Merge.groupbykeys(testobj, keysets))
    print(res)
    assert res == "[{'key': {'fname': 'a', 'lname': 'b'}, 'values': [{'fname': 'a', 'lname': 'b', 'uid': 'hello'}, {'fname': 'a', 'lname': 'b', 'age': 27}, {'fname': 'a', 'lname': 'b', 'gid': 'world'}]}, {'key': {'fname': 'a', 'lname': 'c'}, 'values': [{'fname': 'a', 'lname': 'c', 'uid': 'hi'}, {'fname': 'a', 'lname': 'c', 'age': 22}]}, {'key': {'fname': 'd', 'lname': 'e'}, 'values': [{'fname': 'd', 'lname': 'e', 'uid': 'soup'}, {'fname': 'd', 'lname': 'e', 'gid': 'liquid'}]}, {'key': {'fname': 'f', 'lname': 'e'}, 'values': [{'fname': 'f', 'lname': 'e', 'age': 19}]}]"


def testkeygroup(testobj, keysets):
    res = str(Merge.getkeygroup(testobj, keysets[0]))
    print(res)
    assert res == "[{'fname': 'a', 'lname': 'b', 'uid': 'hello'}, {'fname': 'a', 'lname': 'b', 'age': 27}, {'fname': 'a', 'lname': 'b', 'gid': 'world'}]"


