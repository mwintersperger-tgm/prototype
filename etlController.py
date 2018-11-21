from rules.textRule import TextRule
from rules.idRule import IdRule
from rules.numberRule import NumberRule
from rules.emailRule import EmailRule
from rules.dateRule import DateRule
from rules.patternRule import PatternRule

import json


class ETLController():
    def __init__(self, data):
        self.data = data
        with open('%s' % self.data) as f:
            self.fileData = json.load(f)
        self.loadRules(self.fileData["rules"])
        self.runRules()


    def loadRules(self, rule):
        with open('%s' % rule) as f:
            self.rulesData = json.load(f)
        self.rules = []
        for i in range(len(self.rulesData["rules"])):
            if self.rulesData["rules"][i]["rule"] == "text":
                self.rules.append(TextRule(self.rulesData["rules"][i]["label"], self.rulesData["rules"][i]["minlength"], self.rulesData["rules"][i]["maxlength"], self.rulesData["rules"][i]["letters"]))

            elif self.rulesData["rules"][len(self.rules)]["rule"] == "number":
                self.rules.append(NumberRule(self.rulesData["rules"][i]["label"], self.rulesData["rules"][i]["upper"], self.rulesData["rules"][i]["lower"]))

            elif self.rulesData["rules"][len(self.rules)]["rule"] == "id":
                self.rules.append(IdRule(self.rulesData["rules"][i]["label"]))

            elif self.rulesData["rules"][len(self.rules)]["rule"] == "email":
                self.rules.append(EmailRule(self.rulesData["rules"][i]["label"], self.rulesData["rules"][i]["domain"]))

            elif self.rulesData["rules"][len(self.rules)]["rule"] == "date":
                self.rules.append(DateRule(self.rulesData["rules"][i]["label"], self.rulesData["rules"][i]["pattern"], self.rulesData["rules"][i]["separator"]))

            elif self.rulesData["rules"][len(self.rules)]["rule"] == "pattern":
                self.rules.append(PatternRule(self.rulesData["rules"][i]["label"], self.rulesData["rules"][i]["pattern"]))

    def runRules(self):
        x=0
        for i in range(len(self.fileData["values"][x])-1):
            list = []
            for j in range(len(self.fileData["values"])):
                list.append(self.fileData["values"][j][self.rules[i].getLabel()]["value"])
            x+=1
            print(list)
            print(self.rules[i].validate(list))
