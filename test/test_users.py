import pytest
from userController import UserController
from shutil import copyfile
import os

@pytest.fixture()
def controller():
    user = UserController()
    copyfile("user_ori.json", "user.json")
    yield user
    os.remove("user.json")


def test_addUser(controller):
    controller.addUser("Michael","123Fiona","User","['AU','US']")
    with open("user.json", "r") as f:
        f.readline()
        assert f.readline() == "{\"name\":\"Michael\", \"pswd\":\"123Fiona\", \"type\":\"User\", \"cc\":\"['AU','US']\"}\n"

def test_addUserMessage(controller):
    assert controller.addUser("Michael","123Fiona","User","['AU','US']") == "success"


def test_addUserNonUniqueName(controller):
    controller.addUser("Michael","123Fiona","User","['AU','US']")
    controller.addUser("Michael","123Fiona","User","['AU','US']")
    with open("user.json", "r") as f:
        f.readline()
        f.readline()
        assert f.readline() == "]}"

def test_addUserNonUniqueNameMessage(controller):
    controller.addUser("Michael","123Fiona","User","['AU','US']")
    assert controller.addUser("Michael","123Fiona","User","['AU','US']") == "failure"

def test_listUsernames(controller):
    controller.addUser("Michael1","123Fiona","User","['AU','US']")
    controller.addUser("Michael2","123Fiona","User","['AU','US']")
    assert controller.listUsernames(controller.fileLength()) == ['Michael1', 'Michael2']

def test_removeUser(controller):
    controller.addUser("Michael","123Fiona","User","['AU','US']")
    controller.removeUser("Michael")
    with open("user.json", "r") as f:
        f.readline()
        assert f.readline() == "]}"

def test_checkUser(controller):
    controller.addUser("Michael","123Fiona","User","['AU','US']")
    assert controller.checkUser("Michael","123Fiona") == "{\"name\":\"Michael\", \"pswd\":\"123Fiona\", \"type\":\"User\", \"cc\":\"['AU','US']\"}"
