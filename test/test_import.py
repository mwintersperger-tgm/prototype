from importPkg.importCls import ImportCls
import pytest
import os
import shutil
import json


@pytest.fixture()
def resource():
    print("running setup")
    try:
        # shutil.rmtree(os.path.dirname(os.path.abspath(__file__)) + "\\temp")
        pass
    except Exception as err:
        print(str(err))
    try:
        os.mkdir(os.path.dirname(os.path.abspath(__file__)) + "\\temp")
    except Exception as err:
        print(str(err))
    yield os.path.dirname(os.path.abspath(__file__)) + "/temp/file.txt"
    shutil.rmtree(os.path.dirname(os.path.abspath(__file__)) + "\\temp")


def test_startFile(resource):
    ImportCls.startFile(resource)
    with open(resource) as file:
        obj = json.loads(file.read(os.path.getsize(resource)) + ']}')
        assert obj
        print(str(obj))

def test_endFile(resource):
    with open(resource, "w") as file:
        file.write('{"var":[{},\n')
    ImportCls.endFile(resource)
    with open(resource) as file:
        string = file.read(os.path.getsize(resource))
        print(string)
        obj = json.loads(string)
        assert obj

def test_forward(resource):
    obj = {}
    obj["firstname"] = {}
    obj["firstname"]["value"] = "Alexander"
    obj["firstname"]["validated"] = False
    obj["lastname"] = {}
    obj["lastname"]["value"] = "Alexander"
    obj["lastname"]["validated"] = False
    ImportCls.forward(obj, resource)
    with open(resource) as file:
        string = file.read(os.path.getsize(resource))
        string = string[:len(string) - 2]
        print(string)
        obj = json.loads(string)
        assert obj
