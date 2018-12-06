from exportPkg.exportCls import ExportCls
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