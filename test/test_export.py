import exportPkg.exportCls as ExportCls
import pytest
import os
import shutil
import csv
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
def sampledata():
    data = []
    tmp1 = dict()
    tmp1["firstname"] = {}
    tmp1["firstname"]["value"] = "Alexander"
    tmp1["firstname"]["validated"] = True
    tmp1["lastname"] = {}
    tmp1["lastname"]["value"] = "Kramreiter"
    tmp1["lastname"]["validated"] = True
    tmp2 = dict()
    tmp2["firstname"] = {}
    tmp2["firstname"]["value"] = "Alexander"
    tmp2["firstname"]["validated"] = True
    tmp2["lastname"] = {}
    tmp2["lastname"]["value"] = "Kramreiter"
    tmp2["lastname"]["validated"] = True
    data.append(tmp1)
    data.append(tmp2)
    yield data


def test_csvoutput(resource, sampledata):
    ExportCls.exportcsv(sampledata, resource)
    with open(resource) as file:
        read = csv.reader(file, delimiter="|")
        firstline = True
        listi = []
        for x in read:
            listi.append(x)
        assert isinstance(read, object)

# Don't have an idea how to check if the generated xlsx is valid
