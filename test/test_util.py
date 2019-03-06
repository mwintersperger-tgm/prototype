import importPkg.util as Util
import pytest
import os
import shutil
from pathlib import Path


@pytest.fixture()
def resource():
    print("running setup")
    try:
        os.mkdir(os.path.dirname(os.path.abspath(__file__)) + "\\tmp")
    except Exception as err:
        print(str(err))
    Path("tmp/data1234kappa.json").touch()
    Path("tmp/data23456helloworld.json").touch()
    Path("tmp/data345678sample.json").touch()
    yield os.path.dirname(os.path.abspath(__file__))
    shutil.rmtree(os.path.dirname(os.path.abspath(__file__)) + "\\tmp")


def test_fetchtablenames(resource):
    print(Util.fetchtablenames(resource + "\\tmp"))
    assert True
