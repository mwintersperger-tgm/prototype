from importPkg.importCls import ImportCls
import pytest
import os
import shutil


@pytest.fixture()
def resource():
    print("running setup")
    try:
        os.stat("temp")
    except Exception as err:
        str(err)
        os.mkdir("temp")
    yield "temp"
    shutil.rmtree("temp")


def test_startFile(resource):
    assert 1 == 1