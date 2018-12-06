import unittest
import os
from ruleController import RuleController


class RulesCreation(unittest.TestCase):

    """
    Test the textRule
    """
    def setUp(self):
        self.rules = RuleController()
        self.rules.initRules()

    def tearDown(self):
        os.remove("test.json")

    def test_textRuleCreation(self):
        self.rules.createTextRule("test", 0, 10, ["*"])
        self.rules.createRulesFile("test.json")
        with open("test.json", "r") as f:
            f.readline()
            self.assertEquals(f.readline(), "{\"label\":\"test\", \"rule\":\"text\", \"minlength\":\"0\", \"maxlength\":\"10\", \"letters\":\"['*']\"}\n")

    def test_numberRuleCreation(self):
        self.rules.createNumberRule("test", 18, 25)
        self.rules.createRulesFile("test.json")
        with open("test.json", "r") as f:
            f.readline()
            self.assertEquals(f.readline(), "{\"label\":\"test\", \"rule\":\"number\", \"lower\":\"18\", \"upper\":\"25\"}\n")

    def test_listRuleCreation(self):
        self.rules.createListRule("test", ["test1", "test2"])
        self.rules.createRulesFile("test.json")
        with open("test.json", "r") as f:
            f.readline()
            self.assertEquals(f.readline(), "{\"label\":\"test\", \"rule\":\"list\", \"list\":\"['test1', 'test2']\"}\n")

    def test_dependencyRuleCreation(self):
        self.rules.createDependencyRule("test", {"test1": "bla", "test2": 100}, "test2")
        self.rules.createRulesFile("test.json")
        with open("test.json", "r") as f:
            f.readline()
            self.assertEquals(f.readline(), "{\"label\":\"test\", \"rule\":\"dependency\", \"dict\":{\"test1\": \"bla\", \"test2\": 100}, \"depends\":\"test2\"}\n")

    def test_dateRuleCreation(self):
        self.rules.createDateRule("test", "%d-%m-%Y", "-")
        self.rules.createRulesFile("test.json")
        with open("test.json", "r") as f:
            f.readline()
            self.assertEquals(f.readline(), "{\"label\":\"test\", \"rule\":\"date\", \"pattern\":\"%d-%m-%Y\", \"separator\":\"-\"}\n")

    def test_emailRuleCreation(self):
        self.rules.createEmailRule("test", "at")
        self.rules.createRulesFile("test.json")
        with open("test.json", "r") as f:
            f.readline()
            self.assertEquals(f.readline(), "{\"label\":\"test\", \"rule\":\"email\", \"domain\":\"at\"}\n")

    def test_blankRuleCreation(self):
        self.rules.createBlankRule("test")
        self.rules.createRulesFile("test.json")
        with open("test.json", "r") as f:
            f.readline()
            self.assertEquals(f.readline(), "{\"label\":\"test\", \"rule\":\"blank\"}\n")

    def test_noCommaOnLastLine(self):
        self.rules.createBlankRule("test1")
        self.rules.createBlankRule("test2")
        self.rules.createRulesFile("test.json")
        with open("test.json", "r") as f:
            f.readline()
            f.readline()
            self.assertEquals(f.readline()[-1:], "\n")

    def test_commaOnNonLastLine(self):
        self.rules.createBlankRule("test1")
        self.rules.createBlankRule("test2")
        self.rules.createRulesFile("test.json")
        with open("test.json", "r") as f:
            f.readline()
            self.assertEquals(f.readline()[-2:], ",\n")

    def test_header(self):
        self.rules.createBlankRule("test")
        self.rules.createRulesFile("test.json")
        with open("test.json", "r") as f:
            self.assertEquals(f.readline(), "{\"rules\":[\n")

    def test_lastLine(self):
        self.rules.createBlankRule("test")
        self.rules.createRulesFile("test.json")
        with open("test.json", "r") as f:
            f.readline()
            f.readline()
            self.assertEquals(f.readline(), "]}")
