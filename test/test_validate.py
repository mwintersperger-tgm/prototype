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

def test_textRule():
    textrule = TextRule("test", 0, 10, [])
    assert textrule.validate("test") == True

def test_textRuleTooShort():
    textrule = TextRule("test", 10, 10, [])
    assert textrule.validate("test") == False

def test_textRuleTooLong():
    textrule = TextRule("test", 0, 1, [])
    assert textrule.validate("test") == False

def test_textRuleForbiddenLetter():
    textrule = TextRule("test", 0, 10, ["t"])
    assert textrule.validate("test") == False

def test_textRuleInt():
    textrule = TextRule("test", 0, 10, ["t"])
    assert textrule.validate(10) == True

def test_textRuleNone():
    textrule = TextRule("test", 0, 10, ["t"])
    assert textrule.validate(None) == True

def test_textRuleGetLabel():
    textrule = TextRule("test", 0, 10, ["t"])
    assert textrule.getLabel() == "test"

"""
Test the number rule
"""

def test_numberRule():
    numberrule = NumberRule("test", 10, 0)
    assert numberrule.validate(5) == True

def test_numberRuleTooLow():
    numberrule = NumberRule("test", 10, 10)
    assert numberrule.validate(5) == False

def test_numberRuleTooHigh():
    numberrule = NumberRule("test", 5, 0)
    assert numberrule.validate(10) == False

def test_numberRuleString():
    numberrule = NumberRule("test", 10, 0)
    assert numberrule.validate("a") == False

def test_numberRuleBoolean():
    numberrule = NumberRule("test", 10, 0)
    assert numberrule.validate(True) == False

def test_numberRuleNone():
    numberrule = NumberRule("test", 10, 0)
    assert numberrule.validate(None) == False

def test_numberRuleGetLabel():
    numberrule = NumberRule("test", 0, 10)
    assert numberrule.getLabel() == "test"

"""
Test the date rule
"""

def test_dateRule():
    daterule = DateRule("test", "%d-%m-%Y", "-")
    assert daterule.validate("22-09-2018") == True

def test_dateRuleWrongPattern():
    daterule = DateRule("test", "%d-%m-%Y", "-")
    assert daterule.validate("09-22-2018") == False

def test_dateRuleWrongSeperator():
    daterule = DateRule("test", "%d-%m-%Y", "-")
    assert daterule.validate("22/09/2018") == False

def test_dateRuleInt():
    daterule = DateRule("test", "%d-%m-%Y", "-")
    assert daterule.validate(22092018) == False

def test_dateRuleBool():
    daterule = DateRule("test", "%d-%m-%Y", "-")
    assert daterule.validate(True) == False

def test_dateRuleNone():
    daterule = DateRule("test", "%d-%m-%Y", "-")
    assert daterule.validate(None) == False

def test_dateRuleGetLabel():
    daterule = DateRule("test", "%d-%m-%Y", "-")
    assert daterule.getLabel() == "test"

"""
Test the email rule
"""

def test_emailRule():
    emailrule = EmailRule("test", "at")
    assert emailrule.validate("michael.wintersperger@chello.at") == True

def test_emailRuleWrongDomain():
    emailrule = EmailRule("test", "at")
    assert emailrule.validate("michael.wintersperger@chello.com") == False

def test_emailRuleInvalidEmail():
    emailrule = EmailRule("test", "at")
    assert emailrule.validate("michael.wintersperger.chello.at") == False

def test_emailRuleInt():
    emailrule = EmailRule("test", "at")
    assert emailrule.validate(10) == False

def test_emailRuleBool():
    emailrule = EmailRule("test", "at")
    assert emailrule.validate(True) == False

def test_emailRuleNone():
    emailrule = EmailRule("test", "at")
    assert emailrule.validate(None) == False

def test_emailRuleGetLabel():
    emailrule = EmailRule("test", "at")
    assert emailrule.getLabel() == "test"

"""
Test the list rule
"""

def test_listRule():
    listrule = ListRule("test", "['Schüler','Lehrer']")
    assert listrule.validate("Schüler") == True

def test_listRuleNotInList():
    listrule = ListRule("test", "['Schüler','Leherer']")
    assert listrule.validate("Portier") == False

def test_listRuleNotList():
    listrule = ListRule("test", "10")
    assert listrule.validate("Portier") == False

def test_listRuleGetLabel():
    listrule = ListRule("test", "['Schüler','Leherer']")
    assert listrule.getLabel() == "test"

"""
Test the dependency rule
"""

def test_dependencyRule():
    dependencyrule = DependencyRule("test", {"Anwalt": 500, "Programmierer": 1000}, "test1")
    assert dependencyrule.validate("Anwalt") == 500

def test_dependencyRuleNotInDictonary():
    dependencyrule = DependencyRule("test", {"Anwalt": 500, "Programmierer": 1000}, "test1")
    assert dependencyrule.validate("Kassierer") == None

def test_dependencyRuleGetLabel():
    dependencyrule = DependencyRule("test", {"Anwalt": 500, "Programmierer": 1000}, "test1")
    assert dependencyrule.getLabel() == "test"

def test_dependencyRuleGetDepends():
    dependencyrule = DependencyRule("test", {"Anwalt": 500, "Programmierer": 1000}, "test1")
    assert dependencyrule.getDepends() == "test1"
"""
Test the pattern rule
"""

def test_patternRule():
    patternrule = PatternRule("test", "[0-9]")
    assert patternrule.validate("1") == True

def test_patternRuleNotFitRegex():
    patternrule = PatternRule("test", "[0-9]")
    assert patternrule.validate("a") == False

def test_patternRuleInt():
    patternrule = PatternRule("test", "[0-9]")
    assert patternrule.validate("a") == False

def test_patternRuleBool():
    patternrule = PatternRule("test", "[0-9]")
    assert patternrule.validate(True) == False

def test_patternRuleNone():
    patternrule = PatternRule("test", "[0-9]")
    assert patternrule.validate(None) == False

def test_patternRuleGetLabel():
    patternrule = PatternRule("test", "[0-9]")
    assert patternrule.getLabel() == "test"

"""
Test the blank Rule
"""

def test_blankRule():
    blankrule = BlankRule("test")
    assert blankrule.validate("bla") == True

def test_blankRuleInt():
    blankrule = BlankRule("test")
    assert blankrule.validate(10) == True

def test_blankRuleBool():
    blankrule = BlankRule("test")
    assert blankrule.validate(True) == True

def test_blankRuleNone():
    blankrule = BlankRule("test")
    assert blankrule.validate(None) == True

def test_blankRuleGetLabel():
    blankrule = BlankRule("test")
    assert blankrule.getLabel() == "test"

"""
Test the age Rule
Note: These test results decay as the rule uses datetime.today() as part of its programm
"""

def test_ageRule():
    agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
    assert agerule.validate("22-09-1999") == 19

def test_ageRuleWrongPattern():
    agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
    assert agerule.validate("09-22-1999") == None

def test_ageRuleWrongSeperator():
    agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
    assert agerule.validate("22/09/1999") == None

def test_ageRuleInt():
    agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
    assert agerule.validate(22091999) == None

def test_ageRuleBool():
    agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
    assert agerule.validate(True) == None

def test_ageRuleNone():
    agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
    assert agerule.validate(None) == None

def test_ageRuleGetLabel():
    agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
    assert agerule.getLabel() == "test"

def test_ageRuleGetDepends():
    agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
    assert agerule.getDepends() == "test1"

"""
Test the deadline Rule
Note: These test results decay as the rule uses datetime.today() as part of its programm
"""

def test_deadlineRule():
    deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
    assert deadlinerule.validate("22-09-2019") == "240 days"

def test_deadlineRuleWrongPattern():
    deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
    assert deadlinerule.validate("09-22-2019") == None

def test_deadlineRuleWrongSeperator():
    deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
    assert deadlinerule.validate("22/09/2019") == None

def test_deadlineRuleInt():
    deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
    assert deadlinerule.validate(22092019) == None

def test_deadlineRuleBool():
    deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
    assert deadlinerule.validate(True) == None

def test_deadlineRuleNone():
    deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
    assert deadlinerule.validate(None) == None

def test_deadlineRuleGetLabel():
    deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
    assert deadlinerule.getLabel() == "test"

def test_deadlineRuleGetDepends():
    deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
    assert deadlinerule.getDepends() == "test1"

"""
Test the id Rule
"""

def test_idRule():
    idrule = IdRule("test", "5")
    assert idrule.validate("100") == "00100"

def test_idRuleToLong():
    idrule = IdRule("test", "5")
    assert idrule.validate("100000") == "100000"

def test_idRuleGetLabel():
    idrule = IdRule("test", "5")
    assert idrule.getLabel() == "test"
