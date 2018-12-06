from exportPkg.exportCls import ExportCls
import pytest
import os
import shutil
import csv


@pytest.fixture()
def resource():
    print("running setup")
    try:
        os.stat("/temp")
    except Exception as err:
        str(err)
        os.mkdir("/temp")
    yield "/temp"
    shutil.rmtree("/temp")

@pytest.fixture()
def sampledata():
    data = []
    tmp1 = {}
    tmp1["firstname"] = {}
    tmp1["firstname"]["value"] = "Alexander"
    tmp1["firstname"]["validated"] = True
    tmp1["lastname"] = {}
    tmp1["lastname"]["value"] = "Kramreiter"
    tmp1["lastname"]["validated"] = True
    tmp2 = {}
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
    ExportCls.exportCSV(sampledata, resource)
    with open(resource) as file:
        read = csv.reader(file, delimiter="|")
        firstline = True
        tmp = {}
        print(str(read))
        assert read



# Don't have an idea how to check if the generated xlsx is valid

