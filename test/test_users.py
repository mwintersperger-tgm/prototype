import pytest
from userController import UserController
from shutil import copyfile
import os

@pytest.fixture()
def controller():
    user = UserController()
    copyfile("user_ori.json", "user.json")
    yield user
    #os.remove("user.json")


def test_textRuleCreation(controller):
    controller.addUser("Michael","123Fiona","User","['AU','US']")
    with open("user.json", "r") as f:
        f.readline()
        assert f.readline() == "{\"name\":\"Michael\", \"pswd\":\"123Fiona\", \"type\":\"User\", \"cc\":\"['AU','US']\"}\n"
