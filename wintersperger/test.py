import sys
import unittest
from rules.textRule import TextRule
from rules.numberRule import NumberRule
from rules.emailRule import EmailRule
from rules.dateRule import DateRule
from rules.patternRule import PatternRule
from rules.listRule import ListRule
from rules.dependencyRule import DependencyRule

class RulesValidation(unittest.TestCase):

    '''
    Test the textRule
    '''

    def test_textRule(self):
        textRule = TextRule("test",0,10,[])
        self.assertTrue(textRule.validate("test"))

    def test_textRuleTooShort(self):
        textRule = TextRule("test",10,10,[])
        self.assertFalse(textRule.validate("test"))

    def test_textRuleTooLong(self):
        textRule = TextRule("test",0,1,[])
        self.assertFalse(textRule.validate("test"))

    def test_textRuleForbiddenLetter(self):
        textRule = TextRule("test",0,10,["t"])
        self.assertFalse(textRule.validate("test"))

    def test_textRuleGetLabel(self):
        textRule = TextRule("test",0,10,["t"])
        self.assertEquals(textRule.getLabel(),"test")

    '''
    Test the numberRule
    '''

    def test_numberRule(self):
        numberRule = NumberRule("test",10,0)
        self.assertTrue(numberRule.validate(5))

    def test_numberRuleTooLow(self):
        numberRule = NumberRule("test",10,10)
        self.assertFalse(numberRule.validate(5))

    def test_numberRuleTooHigh(self):
        numberRule = NumberRule("test",5,0)
        self.assertFalse(numberRule.validate(10))

    def test_numberRuleGetLabel(self):
        numberRule = NumberRule("test",0,10)
        self.assertEquals(numberRule.getLabel(),"test")

    '''
    Test the dateRule
    '''

    def test_dateRule(self):
        dateRule = DateRule("test", "%d-%m-%Y", "-" )
        self.assertTrue(dateRule.validate("22-09-2018"))

    def test_dateRuleWrongPattern(self):
        dateRule = DateRule("test", "%d-%m-%Y", "-" )
        self.assertFalse(dateRule.validate("09-22-2018"))

    def test_dateRuleWrongSeperator(self):
        dateRule = DateRule("test", "%d-%m-%Y", "-" )
        self.assertFalse(dateRule.validate("22/09/2018"))

    def test_dateRuleGetLabel(self):
        dateRule = DateRule("test", "%d-%m-%Y", "-" )
        self.assertEquals(dateRule.getLabel(),"test")

    '''
    Test the emailRule
    '''

    def test_emailRule(self):
        emailRule = EmailRule("test", "at" )
        self.assertTrue(emailRule.validate("michael.wintersperger@chello.at"))

    def test_emailRuleWrongDomain(self):
        emailRule = EmailRule("test", "at" )
        self.assertFalse(emailRule.validate("michael.wintersperger@chello.com"))

    def test_emailRuleInvalidEmail(self):
        emailRule = EmailRule("test", "at" )
        self.assertFalse(emailRule.validate("michael.wintersperger.chello.at"))

    def test_emailRuleGetLabel(self):
        emailRule = EmailRule("test", "at" )
        self.assertEquals(emailRule.getLabel(),"test")

    '''
    Test the listRule
    '''

    def test_listRule(self):
        listRule = ListRule("test", ['Schüler','Leherer'] )
        self.assertTrue(listRule.validate("Schüler"))

    def test_listRuleNotInList(self):
        listRule = ListRule("test", "at" )
        self.assertFalse(listRule.validate("Portier"))

    def test_listRuleGetLabel(self):
        listRule = ListRule("test", ['Schüler','Leherer'] )
        self.assertEquals(listRule.getLabel(),"test")

    '''
    Test the dependencyRule
    '''

    def test_dependencyRule(self):
        dependencyRule = DependencyRule("test", {"Anwalt": 500, "Programmierer": 1000}, "test" )
        self.assertEquals(dependencyRule.validate("Anwalt"),500)

    def test_dependencyRuleNotInDictonary(self):
        dependencyRule = DependencyRule("test", {"Anwalt": 500, "Programmierer": 1000}, "test" )
        self.assertEquals(dependencyRule.validate("Anwalt"),None)

    def test_dependencyRuleGetLabel(self):
        dependencyRule = DependencyRule("test", ['Schüler','Leherer'] )
        self.assertEquals(dependencyRule.getLabel(),"test")

    def test_dependencyRuleGetDepends(self):
        dependencyRule = DependencyRule("test", ['Schüler','Leherer'] )
        self.assertEquals(dependencyRule.getDepends(), "test")
    '''
    Test the patternRule
    '''

    def test_patternRule(self):
        patternRule = PatternRule("test", "[0-9]" )
        self.assertTrue(patternRule.validate("1"))

    def test_patternRuleNotFitRegex(self):
        patternRule = PatternRule("test", "[0-9]" )
        self.assertFalse(patternRule.validate("a"))

    def test_patternRuleGetLabel(self):
        patternRule = PatternRule("test", "[0-9]" )
        self.assertEquals(patternRule.getLabel(),"test")
