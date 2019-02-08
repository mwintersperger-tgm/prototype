import unittest
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


class RulesValidation(unittest.TestCase):

    """
    Test the textrule
    """

    def test_textRule(self):
        textrule = TextRule("test", 0, 10, [])
        self.assertTrue(textrule.validate("test"))

    def test_textRuleTooShort(self):
        textrule = TextRule("test", 10, 10, [])
        self.assertFalse(textrule.validate("test"))

    def test_textRuleTooLong(self):
        textrule = TextRule("test", 0, 1, [])
        self.assertFalse(textrule.validate("test"))

    def test_textRuleForbiddenLetter(self):
        textrule = TextRule("test", 0, 10, ["t"])
        self.assertFalse(textrule.validate("test"))

    def test_textRuleInt(self):
        textrule = TextRule("test", 0, 10, ["t"])
        self.assertTrue(textrule.validate(10))

    def test_textRuleNone(self):
        textrule = TextRule("test", 0, 10, ["t"])
        self.assertTrue(textrule.validate(None))

    def test_textRuleGetLabel(self):
        textrule = TextRule("test", 0, 10, ["t"])
        self.assertEquals(textrule.getLabel(), "test")

    """
    Test the number rule
    """

    def test_numberRule(self):
        numberrule = NumberRule("test", 10, 0)
        self.assertTrue(numberrule.validate(5))

    def test_numberRuleTooLow(self):
        numberrule = NumberRule("test", 10, 10)
        self.assertFalse(numberrule.validate(5))

    def test_numberRuleTooHigh(self):
        numberrule = NumberRule("test", 5, 0)
        self.assertFalse(numberrule.validate(10))

    def test_numberRuleString(self):
        numberrule = NumberRule("test", 10, 0)
        self.assertFalse(numberrule.validate("a"))

    def test_numberRuleBoolean(self):
        numberrule = NumberRule("test", 10, 0)
        self.assertFalse(numberrule.validate(True))

    def test_numberRuleNone(self):
        numberrule = NumberRule("test", 10, 0)
        self.assertFalse(numberrule.validate(None))

    def test_numberRuleGetLabel(self):
        numberrule = NumberRule("test", 0, 10)
        self.assertEquals(numberrule.getLabel(), "test")

    """
    Test the date rule
    """

    def test_dateRule(self):
        daterule = DateRule("test", "%d-%m-%Y", "-")
        self.assertTrue(daterule.validate("22-09-2018"))

    def test_dateRuleWrongPattern(self):
        daterule = DateRule("test", "%d-%m-%Y", "-")
        self.assertFalse(daterule.validate("09-22-2018"))

    def test_dateRuleWrongSeperator(self):
        daterule = DateRule("test", "%d-%m-%Y", "-")
        self.assertFalse(daterule.validate("22/09/2018"))

    def test_dateRuleInt(self):
        daterule = DateRule("test", "%d-%m-%Y", "-")
        self.assertFalse(daterule.validate(22092018))

    def test_dateRuleBool(self):
        daterule = DateRule("test", "%d-%m-%Y", "-")
        self.assertFalse(daterule.validate(True))

    def test_dateRuleNone(self):
        daterule = DateRule("test", "%d-%m-%Y", "-")
        self.assertFalse(daterule.validate(None))

    def test_dateRuleGetLabel(self):
        daterule = DateRule("test", "%d-%m-%Y", "-")
        self.assertEquals(daterule.getLabel(), "test")

    """
    Test the email rule
    """

    def test_emailRule(self):
        emailrule = EmailRule("test", "at")
        self.assertTrue(emailrule.validate("michael.wintersperger@chello.at"))

    def test_emailRuleWrongDomain(self):
        emailrule = EmailRule("test", "at")
        self.assertFalse(emailrule.validate("michael.wintersperger@chello.com"))

    def test_emailRuleInvalidEmail(self):
        emailrule = EmailRule("test", "at")
        self.assertFalse(emailrule.validate("michael.wintersperger.chello.at"))

    def test_emailRuleInt(self):
        emailrule = EmailRule("test", "at")
        self.assertFalse(emailrule.validate(10))

    def test_emailRuleBool(self):
        emailrule = EmailRule("test", "at")
        self.assertFalse(emailrule.validate(True))

    def test_emailRuleNone(self):
        emailrule = EmailRule("test", "at")
        self.assertFalse(emailrule.validate(None))

    def test_emailRuleGetLabel(self):
        emailrule = EmailRule("test", "at")
        self.assertEquals(emailrule.getLabel(), "test")

    """
    Test the list rule
    """

    def test_listRule(self):
        listrule = ListRule("test", "['Schüler','Lehrer']")
        self.assertTrue(listrule.validate("Schüler"))

    def test_listRuleNotInList(self):
        listrule = ListRule("test", "['Schüler','Leherer']")
        self.assertFalse(listrule.validate("Portier"))

    def test_listRuleNotList(self):
        listrule = ListRule("test", "10")
        self.assertFalse(listrule.validate("Portier"))

    def test_listRuleGetLabel(self):
        listrule = ListRule("test", "['Schüler','Leherer']")
        self.assertEquals(listrule.getLabel(), "test")

    """
    Test the dependency rule
    """

    def test_dependencyRule(self):
        dependencyrule = DependencyRule("test", {"Anwalt": 500, "Programmierer": 1000}, "test1")
        self.assertEquals(dependencyrule.validate("Anwalt"), 500)

    def test_dependencyRuleNotInDictonary(self):
        dependencyrule = DependencyRule("test", {"Anwalt": 500, "Programmierer": 1000}, "test1")
        self.assertEquals(dependencyrule.validate("Kassierer"), None)

    def test_dependencyRuleGetLabel(self):
        dependencyrule = DependencyRule("test", {"Anwalt": 500, "Programmierer": 1000}, "test1")
        self.assertEquals(dependencyrule.getLabel(), "test")

    def test_dependencyRuleGetDepends(self):
        dependencyrule = DependencyRule("test", {"Anwalt": 500, "Programmierer": 1000}, "test1")
        self.assertEquals(dependencyrule.getDepends(), "test1")
    """
    Test the pattern rule
    """

    def test_patternRule(self):
        patternrule = PatternRule("test", "[0-9]")
        self.assertTrue(patternrule.validate("1"))

    def test_patternRuleNotFitRegex(self):
        patternrule = PatternRule("test", "[0-9]")
        self.assertFalse(patternrule.validate("a"))

    def test_patternRuleInt(self):
        patternrule = PatternRule("test", "[0-9]")
        self.assertFalse(patternrule.validate("a"))

    def test_patternRuleBool(self):
        patternrule = PatternRule("test", "[0-9]")
        self.assertFalse(patternrule.validate(True))

    def test_patternRuleNone(self):
        patternrule = PatternRule("test", "[0-9]")
        self.assertFalse(patternrule.validate(None))

    def test_patternRuleGetLabel(self):
        patternrule = PatternRule("test", "[0-9]")
        self.assertEquals(patternrule.getLabel(), "test")

    """
    Test the blank Rule
    """

    def test_blankRule(self):
        blankrule = BlankRule("test")
        self.assertTrue(blankrule.validate("bla"))

    def test_blankRuleInt(self):
        blankrule = BlankRule("test")
        self.assertTrue(blankrule.validate(10))

    def test_blankRuleBool(self):
        blankrule = BlankRule("test")
        self.assertTrue(blankrule.validate(True))

    def test_blankRuleNone(self):
        blankrule = BlankRule("test")
        self.assertTrue(blankrule.validate(None))

    def test_blankRuleGetLabel(self):
        blankrule = BlankRule("test")
        self.assertEquals(blankrule.getLabel(), "test")

    """
    Test the age Rule
    Note: These test results decay as the rule uses datetime.today() as part of its programm
    """

    def test_ageRule(self):
        agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
        self.assertEquals(agerule.validate("22-09-1999"),19)

    def test_ageRuleWrongPattern(self):
        agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
        self.assertEquals(agerule.validate("09-22-1999"), None)

    def test_ageRuleWrongSeperator(self):
        agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
        self.assertEquals(agerule.validate("22/09/1999"), None)

    def test_ageRuleInt(self):
        agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
        self.assertEquals(agerule.validate(22091999), None)

    def test_ageRuleBool(self):
        agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
        self.assertEquals(agerule.validate(True), None)

    def test_ageRuleNone(self):
        agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
        self.assertEquals(agerule.validate(None), None)

    def test_ageRuleGetLabel(self):
        agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
        self.assertEquals(agerule.getLabel(), "test")

    def test_ageRuleGetDepends(self):
        agerule = AgeRule("test", "test1", "%d-%m-%Y", "-")
        self.assertEquals(agerule.getDepends(), "test1")

    """
    Test the deadline Rule
    Note: These test results decay as the rule uses datetime.today() as part of its programm
    """

    def test_deadlineRule(self):
        deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
        self.assertEquals(deadlinerule.validate("22-09-2019"),"240 days")

    def test_deadlineRuleWrongPattern(self):
        deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
        self.assertEquals(deadlinerule.validate("09-22-2019"), None)

    def test_deadlineRuleWrongSeperator(self):
        deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
        self.assertEquals(deadlinerule.validate("22/09/2019"), None)

    def test_deadlineRuleInt(self):
        deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
        self.assertEquals(deadlinerule.validate(22092019), None)

    def test_deadlineRuleBool(self):
        deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
        self.assertEquals(deadlinerule.validate(True), None)

    def test_deadlineRuleNone(self):
        deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
        self.assertEquals(deadlinerule.validate(None), None)

    def test_deadlineRuleGetLabel(self):
        deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
        self.assertEquals(deadlinerule.getLabel(), "test")

    def test_deadlineRuleGetDepends(self):
        deadlinerule = DeadlineRule("test", "test1", "%d-%m-%Y", "-")
        self.assertEquals(deadlinerule.getDepends(), "test1")

    """
    Test the id Rule
    """

    def test_idRule(self):
        idrule = IdRule("test", "5")
        self.assertEquals(idrule.validate("100"),"00100")

    def test_idRuleToLong(self):
        idrule = IdRule("test", "5")
        self.assertEquals(idrule.validate("100000"),"100000")

    def test_idRuleGetLabel(self):
        idrule = IdRule("test", "5")
        self.assertEquals(idrule.getLabel(), "test")
