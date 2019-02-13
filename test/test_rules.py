import pytest
import os
from ruleController import RuleController


@pytest.fixture()
def controller():
    rules = RuleController()
    rules.initRules()
    yield rules
    os.remove("test.json")

def test_textRuleCreation(controller):
    controller.createTextRule("test", 0, 10, ["*"])
    controller.createRulesFile("test.json")
    with open("test.json", "r") as f:
        f.readline()
        assert f.readline() == "{\"label\":\"test\", \"rule\":\"text\", \"minlength\":\"0\", \"maxlength\":\"10\", \"letters\":\"['*']\"}\n"

def test_numberRuleCreation(controller):
    controller.createNumberRule("test", 18, 25)
    controller.createRulesFile("test.json")
    with open("test.json", "r") as f:
        f.readline()
        assert f.readline() == "{\"label\":\"test\", \"rule\":\"number\", \"lower\":\"18\", \"upper\":\"25\"}\n"

def test_listRuleCreation(controller):
    controller.createListRule("test", ["test1", "test2"])
    controller.createRulesFile("test.json")
    with open("test.json", "r") as f:
        f.readline()
        assert f.readline() == "{\"label\":\"test\", \"rule\":\"list\", \"list\":\"['test1', 'test2']\"}\n"

def test_dependencyRuleCreation(controller):
    controller.createDependencyRule("test", {"test1": "bla", "test2": 100}, "test2")
    controller.createRulesFile("test.json")
    with open("test.json", "r") as f:
        f.readline()
        assert f.readline() == "{\"label\":\"test\", \"rule\":\"dependency\", \"dict\":{\"test1\": \"bla\", \"test2\": 100}, \"depends\":\"test2\"}\n"

def test_dateRuleCreation(controller):
    controller.createDateRule("test", "%d-%m-%Y", "-")
    controller.createRulesFile("test.json")
    with open("test.json", "r") as f:
        f.readline()
        assert f.readline() == "{\"label\":\"test\", \"rule\":\"date\", \"pattern\":\"%d-%m-%Y\", \"separator\":\"-\"}\n"

def test_emailRuleCreation(controller):
    controller.createEmailRule("test", "at")
    controller.createRulesFile("test.json")
    with open("test.json", "r") as f:
        f.readline()
        assert f.readline() == "{\"label\":\"test\", \"rule\":\"email\", \"domain\":\"at\"}\n"

def test_blankRuleCreation(controller):
    controller.createBlankRule("test")
    controller.createRulesFile("test.json")
    with open("test.json", "r") as f:
        f.readline()
        assert f.readline() == "{\"label\":\"test\", \"rule\":\"blank\"}\n"

def test_ageRuleCreation(controller):
    controller.createAgeRule("test", "test1", "%d-%m-%Y", "-")
    controller.createRulesFile("test.json")
    with open("test.json", "r") as f:
        f.readline()
        assert f.readline() == "{\"label\":\"test\", \"rule\":\"age\", \"pattern\":\"%d-%m-%Y\", \"separator\":\"-\", \"depends\":\"test1\"}\n"

def test_deadlineRuleCreation(controller):
    controller.createDeadlineRule("test", "test1", "%d-%m-%Y", "-")
    controller.createRulesFile("test.json")
    with open("test.json", "r") as f:
        f.readline()
        assert f.readline() == "{\"label\":\"test\", \"rule\":\"deadline\", \"pattern\":\"%d-%m-%Y\", \"separator\":\"-\", \"depends\":\"test1\"}\n"

def test_patternRuleCreation(controller):
    controller.createPatternRule("test", "[0-9A-Fa-f]*")
    controller.createRulesFile("test.json")
    with open("test.json", "r") as f:
        f.readline()
        assert f.readline() == "{\"label\":\"test\", \"rule\":\"pattern\", \"pattern\":\"[0-9A-Fa-f]*\"}\n"

def test_idRuleCreation(controller):
    controller.createIdRule("test", "5")
    controller.createRulesFile("test.json")
    with open("test.json", "r") as f:
        f.readline()
        assert f.readline() == "{\"label\":\"test\", \"rule\":\"id\", \"digits\":\"5\"}\n"

def test_noCommaOnLastLine(controller):
    controller.createBlankRule("test1")
    controller.createBlankRule("test2")
    controller.createRulesFile("test.json")
    with open("test.json", "r") as f:
        f.readline()
        f.readline()
        assert f.readline()[-1:] == "\n"

def test_commaOnNonLastLine(controller):
    controller.createBlankRule("test1")
    controller.createBlankRule("test2")
    controller.createRulesFile("test.json")
    with open("test.json", "r") as f:
        f.readline()
        assert f.readline()[-2:] == ",\n"

def test_header(controller):
    controller.createBlankRule("test")
    controller.createRulesFile("test.json")
    with open("test.json", "r") as f:
        assert f.readline() == "{\"rules\":[\n"

def test_lastLine(controller):
    controller.createBlankRule("test")
    controller.createRulesFile("test.json")
    with open("test.json", "r") as f:
        f.readline()
        f.readline()
        assert f.readline() == "]}"
