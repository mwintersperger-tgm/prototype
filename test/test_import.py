import importPkg.importCls as ImportCls
import pytest
import os
import shutil
import json
from pandas import DataFrame


@pytest.fixture()
def resource():
    print("running setup")
    try:
        os.mkdir(os.path.dirname(os.path.abspath(__file__)) + "\\tmp")
    except Exception as err:
        print(str(err))
    yield os.path.dirname(os.path.abspath(__file__)) + "/tmp/file.txt"
    try:
        shutil.rmtree(os.path.dirname(os.path.abspath(__file__)) + "\\tmp")
    except Exception as err:
        print(str(err))


@pytest.fixture()
def resource2():
    print("running setup")
    try:
        os.mkdir(os.path.dirname(os.path.abspath(__file__)) + "\\tmp2")
    except Exception as err:
        print(str(err))
    yield os.path.dirname(os.path.abspath(__file__)) + "/tmp2/file.txt"
    try:
        shutil.rmtree(os.path.dirname(os.path.abspath(__file__)) + "\\tmp2")
    except Exception as err:
        print(str(err))


@pytest.fixture()
def testobject():
    obj = dict()
    obj["firstname"] = {}
    obj["firstname"]["value"] = "Alexander"
    obj["firstname"]["validated"] = False
    obj["lastname"] = {}
    obj["lastname"]["value"] = "Kramreiter"
    obj["lastname"]["validated"] = False
    yield obj


@pytest.fixture()
def testmapping():
    obj = dict()
    obj["firstname"] = "fname"
    obj["lastname"] = "lname"
    yield obj


@pytest.fixture()
def resource3():
    try:
        os.mkdir(os.path.dirname(os.path.abspath(__file__)) + "\\tmp")
    except Exception as err:
        print(str(err))
    cols = dict()
    cols['fname'] = []
    cols['lname'] = []
    cols['fname'].append('Alexander')
    cols['fname'].append('Michael')
    cols['fname'].append('Thomas')
    cols['fname'].append('Benjamin')
    cols['lname'].append('Kramreiter')
    cols['lname'].append('Wintersperger')
    cols['lname'].append('Schweder')
    cols['lname'].append('Rasic')
    frame = DataFrame(cols)
    path = os.path.dirname(os.path.abspath(__file__)) + "\\tmp\\file.xlsx"
    frame.to_excel(path, sheet_name="test", index=False)
    yield path
    try:
        shutil.rmtree(os.path.dirname(os.path.abspath(__file__)) + "\\tmp")
    except Exception as err:
        print(str(err))


def test_startfile(resource):
    ImportCls.start_file(resource)
    with open(resource) as file:
        obj = json.loads(file.read() + ']}')
        assert obj
        print(str(obj))


def test_endfile(resource):
    with open(resource, "w") as file:
        file.truncate(0)
        file.write("{\"var\":[{},\n")
    ImportCls.end_file(resource)
    with open(resource) as file:
        string = file.read()
        print(string)
        obj = json.loads(string)
        assert obj


def test_forward(resource, testobject):
    obj = testobject
    ImportCls.forward(obj, resource)
    with open(resource) as file:
        string = file.read()
        string = string[:len(string) - 2]
        print(string)
        obj = json.loads(string)
        assert obj


def testcombined(resource, testobject):
    ImportCls.start_file(resource)
    ImportCls.forward(testobject, resource)
    ImportCls.end_file(resource)
    with open(resource) as file:
        string = file.read()
        print(string)
        obj = json.loads(string)
        assert obj


def testvalidatemapping(testmapping, resource2):
    print("saving mapping")
    print(testmapping)
    assert ImportCls.savemapping(testmapping, resource2)


def testvalidatemappingwrongtype(testmapping, resource2):
    print("failing to save mapping with wrong type")
    testmapping["hi"] = 12
    print(testmapping)
    assert not ImportCls.savemapping(testmapping, resource2)


def testvalidatemappingempty(resource2):
    print("failing to save empty mapping")
    assert not ImportCls.savemapping({}, resource2)


def testvalidatemappingdupe(testmapping, resource2):
    print("failing to save mapping with duplicate value to map to")
    testmapping["secondname"] = "fname"
    print(testmapping)
    assert not ImportCls.savemapping(testmapping, resource2)


def testvalidatemappingnotdict(resource2):
    print("failing to save mapping that isn't a dict")
    testmapping = "Hello World!"
    print(testmapping)
    assert not ImportCls.savemapping(testmapping, resource2)


def testsafemapping(testmapping, resource2):
    print("saving mapping")
    print(testmapping)
    ImportCls.savemapping(testmapping, resource2)
    with open(resource2) as file:
        assert len(file.read()) == len(json.dumps(testmapping))


def testloadmapping(testmapping, resource2):
    print("saving mapping")
    print(testmapping)
    ImportCls.savemapping(testmapping, resource2)
    print("checking if loadmapping is retrieving it properly")
    assert ImportCls.loadmapping(resource2) == testmapping


def testloadforinvalidfile(resource2):
    with open(resource2, "w") as file:
        obj = dict()
        obj["hi"] = 0
        print("manually writing invalid file")
        print(obj)
        file.truncate(0)
        file.write(json.dumps(obj))
    print("checking if invalid file is NOT loaded")
    assert ImportCls.loadmapping(resource2) is None


def testimportxlsx(resource3):
    ImportCls.importxlsx(resource3, resource3)
    with open(resource3) as file:
        res = json.loads(file.read())
    assert res['values'] == [{'fname': {'value': 'Alexander', 'validated': False}, 'lname': {'value': 'Kramreiter', 'validated': False}}, {'fname': {'value': 'Michael', 'validated': False}, 'lname': {'value': 'Wintersperger', 'validated': False}}, {'fname': {'value': 'Thomas', 'validated': False}, 'lname': {'value': 'Schweder', 'validated': False}}, {'fname': {'value': 'Benjamin', 'validated': False}, 'lname': {'value': 'Rasic', 'validated': False}}]
