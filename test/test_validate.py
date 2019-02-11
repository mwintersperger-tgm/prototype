import pytest
from rules.textRule import TextRule
from rules.numberRule import NumberRule
from rules.emailRule import EmailRule
from rules.dateRule import DateRule
from rules.patternRule import PatternRule
from rules.listRule import ListRule
from rules.dependencyRule import DependencyRule
from rules.blankRule import BlankRule
from rules.ageRule import AgeRule
from rules.deadlineRule import DeadlineRule
from rules.idRule import IdRule


"""
Test the textrule
"""

def test_textRule(self):
    textrule = TextRule("test", 0, 10, [])
    assert textrule.validate("test") == True

def test_textRuleTooShort(self):
    textrule = TextRule("test", 10, 10, [])
    assert textrule.validate("test") == False

def test_textRuleTooLong(self):
    textrule = TextRule("test", 0, 1, [])
    assert textrule.validate("test") == False

def test_textRuleForbiddenLetter(self):
    textrule = TextRule("test", 0, 10, ["t"])
    assert textrule.validate("test") == False

def test_textRuleInt(self):
    textrule = TextRule("test", 0, 10, ["t"])
    assert textrule.validate(10) == True

def test_textRuleNone(self):
    textrule = TextRule("test", 0, 10, ["t"])
    assert textrule.validate(None) == True

def test_textRuleGetLabel(self):
    textrule = TextRule("test", 0, 10, ["t"])
    assert textrule.getLabel() == "test"

"""
Test the number rule
"""

def test_numberRule(self):
    numberrule = NumberRule("test", 10, 0)
    assert numberrule.validate(5) == True

def test_numberRuleTooLow(self):
    numberrule = NumberRule("test", 10, 10)
    assert numberrule.validate(5) == False

def test_numberRuleTooHigh(self):
    numberrule = NumberRule("test", 5, 0)
    assert numberrule.validate(10) == False

def test_numberRuleString(self):
    numberrule = NumberRule("test", 10, 0)
    assert numberrule.validate("a") == False

def test_numberRuleBoolean(self):
    numberrule = NumberRule("test", 10, 0)
    assert numberrule.validate(True) == False

def test_numberRuleNone(self):
    numberrule = NumberRule("test", 10, 0)
    assert numberrule.validate(None) == False

def test_numberRuleGetLabel(self):
    numberrule = NumberRule("test", 0, 10)
    assert numberrule.getLabel() == "test"

"""
Test the date rule
"""

def test_dateRule(self):
    daterule = DateRule("test", "%d-%m-%Y", "-")
    assert daterule.validate("22-09-2018") == True

def test_dateRuleWrongPattern(self):
    daterule = DateRule("test", "%d-%m-%Y", "-")
    assert daterule.validate("09-22-2018") == False

def test_dateRuleWrongSeperator(self):
    daterule = DateRule("test", "%d-%m-%Y", "-")
    assert daterule.validate("22/09/2018") == False

def test_dateRuleInt(self):
    daterule = DateRule("test", "%d-%m-%Y", "-")
    assert daterule.validate(22092018) == False

def test_dateRuleBool(self):
    daterule = DateRule("test", "%d-%m-%Y", "-")
    assert daterule.validate(True) == False

def test_dateRuleNone(self):
    daterule = DateRule("test", "%d-%m-%Y", "-")
    assert daterule.validate(None) == False

def test_dateRuleGetLabel(self):
    daterule = DateRule("test", "%d-%m-%Y", "-")
    assert daterule.getLabel() == "test"

"""
Test the email rule
"""

def test_emailRule(self):
    emailrule = EmailRule("test", "at")
    assert emailrule.validate("michael.wintersperger@chello.at") == True

def test_emailRuleWrongDomain(self):
    emailrule = EmailRule("test", "at")
    assert emailrule.validate("michael.wintersperger@chello.com") == False

def test_emailRuleInvalidEmail(self):
    emailrule = EmailRule("test", "at")
    assert emailrule.validate("michael.wintersperger.chello.at") == False

def test_emailRuleInt(self):
    emailrule = EmailRule("test", "at")
    assert emailrule.validate(10) == False

def test_emailRuleBool(self):
    emailrule = EmailRule("test", "at")
    assert emailrule.validate(True) == False

def test_emailRuleNone(self):
    emailrule = EmailRule("test", "at")
    assert emailrule.validate(None) == False

def test_emailRuleGetLabel(self):
    emailrule = EmailRule("test", "at")
    assert emailrule.getLabel() == "test"

"""
Test the list rule
"""

def test_listRule(self):
    listrule = ListRule("test", "['Schüler','Lehrer']")
    assert listrule.validate("Schüler") == True

def test_listRuleNotInList(self):
    listrule = ListRule("test", "['Schüler','Leherer']")
    assert listrule.validate("Portier") == False

def test_listRuleNotList(self):
    listrule = ListRule("test", "10")
    assert listrule.validate("Portier") == False

def test_listRuleGetLabel(self):
    listrule = ListRule("test", "['Schüler','Leherer']")
    assert listrule.getLabel() == "test"

"""
Test the dependency rule
"""

def test_dependencyRule(self):
    dependencyrule = DependencyRule("test", {"Anwalt": 500, "Programmierer": 1000}, "test1")
    assert dependencyrule.validate("Anwalt") == 500

def test_dependencyRuleNotInDictonary(self):
    dependencyrule = DependencyRule("test", {"Anwalt": 500, "Programmierer": 1000}, "test1")
    assert dependencyrule.validate("Kassierer") == None

def test_dependencyRuleGetLabel(self):
    dependencyrule = DependencyRule("test", {"Anwalt": 500, "Programmierer": 1000}, "test1")
    assert dependencyrule.getLabel() == "test"

def test_dependencyRuleGetDepends(self):
    dependencyrule = DependencyRule("test", {"Anwalt": 500, "Programmierer": 1000}, "test1")
    assert dependencyrule.getDepends() == "test1"
"""
Test the pattern rule
"""

def test_patternRule(self):
    patternrule = PatternRule("test", "[0-9]")
    assert patternrule.validate("1") == True

def test_patternRuleNotFitRegex(self):
    patternrule = PatternRule("test", "[0-9]")
    assert patternrule.validate("a") == False

def test_patternRuleInt(self):
    patternrule = PatternRule("test", "[0-9]")
    assert patternrule.validate("a") == False

def test_patternRuleBool(self):
    patternrule = PatternRule("test", "[0-9]")
    assert patternrule.validate(True) == False

def test_patternRuleNone(self):
    patternrule = PatternRule("test", "[0-9]")
    assert patternrule.validate(None) == False

def test_patternRuleGetLabel(self):
    patternrule = PatternRule("test", "[0-9]")
    assert patternrule.getLabel(), "test")

"""
Test the blank Rule
"""

def test_blankRule(self):
    blankrule = BlankRule("test")
    assert blankrule.validate("bla") == True

def test_blankRuleInt(self):
    blankrule = BlankRule("test")
    assert blankrule.validate(10) == True

def test_blankRuleBool(self):
    blankrule = BlankRule("test")
    assert blankrule.validate(True) == True

def test_blankRuleNone(self):
    blankrule = BlankRule("test")
    assert blankrule.validate(None) == True

def test_blankRuleGetLabel(self):
    blankrule = BlankRule("test")
    assert blankrule.getLabel(), "test")

"""
Test the age Rule
Note: These test results decay as the rule uses datetime.today() as part of its programm
"""

def test_ageRule(self):
    agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
    assert agerule.validate("22-09-1999"),19)

def test_ageRuleWrongPattern(self):
    agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
    assert agerule.validate("09-22-1999"), None)

def test_ageRuleWrongSeperator(self):
    agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
    assert agerule.validate("22/09/1999"), None)

def test_ageRuleInt(self):
    agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
    assert agerule.validate(22091999), None)

def test_ageRuleBool(self):
    agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
    assert agerule.validate(True), None)

def test_ageRuleNone(self):
    agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
    assert agerule.validate(None), None)

def test_ageRuleGetLabel(self):
    agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
    assert agerule.getLabel(), "test")

def test_ageRuleGetDepends(self):
    agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
    assert agerule.getDepends(), "test1")

"""
Test the deadline Rule
Note: These test results decay as the rule uses datetime.today() as part of its programm
"""

def test_deadlineRule(self):
    deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
    assert deadlinerule.validate("22-09-2019"),"240 days")

def test_deadlineRuleWrongPattern(self):
    deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
    assert deadlinerule.validate("09-22-2019"), None)

def test_deadlineRuleWrongSeperator(self):
    deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
    assert deadlinerule.validate("22/09/2019"), None)

def test_deadlineRuleInt(self):
    deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
    assert deadlinerule.validate(22092019), None)

def test_deadlineRuleBool(self):
    deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
    assert deadlinerule.validate(True), None)

def test_deadlineRuleNone(self):
    deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
    assert deadlinerule.validate(None), None)

def test_deadlineRuleGetLabel(self):
    deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
    assert deadlinerule.getLabel(), "test")

def test_deadlineRuleGetDepends(self):
    deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
    assert deadlinerule.getDepends(), "test1")

"""
Test the id Rule
"""

def test_idRule(self):
    idrule = IdRule("test", "5")
    assert idrule.validate("100"),"00100")

def test_idRuleToLong(self):
    idrule = IdRule("test", "5")
    assert idrule.validate("100000"),"100000")

def test_idRuleGetLabel(self):
    idrule = IdRule("test", "5")
    assert idrule.getLabel(), "test")
