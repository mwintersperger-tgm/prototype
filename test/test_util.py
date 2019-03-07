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
    assert Util.fetchtablenames(resource + "\\tmp") == ['kappa', 'helloworld', 'sample']


def test_fetchdatafilenames(resource):
    assert Util.fetchdatafilenames(resource + "\\tmp") == ['data1234kappa.json', 'data23456helloworld.json', 'data345678sample.json']


def test_fetchnameforfile():
    assert Util.fetchtnameforfile('data1234kappa.json') == 'kappa'
