import importPkg.util as Util
import pytest
import os
import shutil


@pytest.fixture()
def resource():
    print("running setup")
    try:
        os.mkdir(os.path.dirname(os.path.abspath(__file__)) + "\\tmp")
        open(os.path.abspath(__file__) + "\\tmp\\data1234kappa.json", 'a').close()
        open(os.path.abspath(__file__) + "\\tmp\\data23456helloworld.json", 'a').close()
        open(os.path.abspath(__file__) + "\\tmp\\data345678sample.json", 'a').close()
    except Exception as err:
        print(str(err))
    yield os.path.dirname(os.path.abspath(__file__))
    shutil.rmtree(os.path.dirname(os.path.abspath(__file__)) + "\\tmp")


def test_fetchtablenames(resource):
    Util.fetchtablenames(resource + "\\tmp")
    assert True
