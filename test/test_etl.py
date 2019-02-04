import unittest
import os
import shutil
import filecmp
import json

from etlController import ETLController

class etlFunctions(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        self.etl = ETLController()
        shutil.copyfile('data_original.json', 'data.json')

    def tearDown(self):
        os.remove("data.json")

    def test_getLabels(self):
        self.assertEquals(self.etl.getLabels('data.json'),['firstname','lastname','age','job','income','birthday','email'])

    def test_getCC(self):
        self.assertEquals(self.etl.getCC('data.json'),'EN')

    def test_setCC(self):
        self.etl.setCC('data.json','AUS')
        self.assertEquals(self.etl.getCC('data.json'),'AUS')

    def test_getRule(self):
        self.assertEquals(self.etl.getRule('data.json'),'rule.json')

    def test_setRule(self):
        self.etl.setRule('data.json','test.json')
        self.assertEquals(self.etl.getRule('data.json'),'test.json')

    def test_fileLength(self):
        self.assertEquals(self.etl.fileLength('data.json'),5)

    def test_runRules(self):
        self.etl.runRules('data.json',0,3)
        self.assertTrue(filecmp.cmp('data.json','validated.json'))

    def test_simpleReplace(self):
        self.etl.simpleReplace('data.json','firstname',{'*':''})
        with open("data.json", "r") as f:
            f.readline()
            f.readline()
            f.readline()
            line = str(f.readline())
            data = line[25:line.find(',')-1]
            self.assertEquals(data, "Michael")
