from importPkg.importCls import ImportCls
import pytest
import os
import shutil
import json


@pytest.fixture()
def resource():
    print("running setup")
    try:
        os.mkdir(os.path.dirname(os.path.abspath(__file__)) + "\\tmp")
    except Exception as err:
        print(str(err))
    yield os.path.dirname(os.path.abspath(__file__)) + "/tmp/file.txt"
    shutil.rmtree(os.path.dirname(os.path.abspath(__file__)) + "\\tmp")

@pytest.fixture()
def testobject():
    obj = {}
    obj["firstname"] = {}
    obj["firstname"]["value"] = "Alexander"
    obj["firstname"]["validated"] = False
    obj["lastname"] = {}
    obj["lastname"]["value"] = "Kramreiter"
    obj["lastname"]["validated"] = False
    yield obj

def test_startFile(resource):
    ImportCls.startFile(resource)
    with open(resource) as file:
        obj = json.loads(file.read() + ']}')
        assert obj
        print(str(obj))


def test_endFile(resource):
    with open(resource, "w") as file:
        file.write('{"var":[{},\n')
    ImportCls.endFile(resource)
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
    ImportCls.startFile(resource)
    ImportCls.forward(testobject, resource)
    ImportCls.endFile(resource)
    with open(resource) as file:
        string = file.read()
        print(string)
        obj = json.loads(string)
        assert obj