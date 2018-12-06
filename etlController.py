from rules.textRule import TextRule
from rules.numberRule import NumberRule
from rules.emailRule import EmailRule
from rules.dateRule import DateRule
from rules.patternRule import PatternRule
from rules.listRule import ListRule
from rules.dependencyRule import DependencyRule

import json
import os

class ETLController():
    def loadRules(self, data):
        self.rules = []
        rulename = self.getRules(data)
        filelen = self.linesJson(rulename)
        with open(rulename, "r") as f:
            rule={}
            f.readline()
            for i in range(1,filelen-1):
                rule=json.loads(f.readline().rstrip(",\n"))
                if rule["rule"] == "text":
                    self.rules.append(TextRule(str(rule["label"]), int(rule["minlength"]), int(rule["maxlength"]), str(rule["letters"])))

                elif rule["rule"] == "number":
                    self.rules.append(NumberRule(str(rule["label"]), int(rule["upper"]), int(rule["lower"])))

                elif rule["rule"] == "email":
                    self.rules.append(EmailRule(str(rule["label"]), str(rule["domain"])))

                elif rule["rule"] == "date":
                    self.rules.append(DateRule(str(rule["label"]), str(rule["pattern"]), str(rule["separator"])))

                elif rule["rule"] == "pattern":
                    self.rules.append(PatternRule(str(rule["label"]), str(rule["pattern"])))

                elif rule["rule"] == "list":
                    self.rules.append(ListRule(str(rule["label"]), rule["list"]))

                elif rule["rule"] == "dependency":
                    self.rules.append(DependencyRule(str(rule["label"]), rule["dict"], rule["depends"]))

    def setRules(self,filename,rule):
        newfile = filename[:filename.rfind('/')+1]+"new_"+filename[filename.rfind('/')+1:]
        filelen = self.linesJson(filename)
        with open("%s" % filename,"r") as of:
            of.readline()
            with open("%s" % newfile, "w") as nf:
                line='{"rules":"%s", "values":[\n' % rule
                nf.write(line)
                for i in range(1,filelen):
                    line = of.readline()
                    nf.write(line)
        os.remove(filename)
        os.rename(newfile, filename)

    def getRules(self,filename):
        with open("%s" % filename, "r") as f:
            rule = f.readline()
            rule = rule[10:-14]
            return rule

    def linesJson(self, filename):
        num_lines = sum(1 for line in open(filename))
        return  num_lines

    def runRules(self, filename, start=0, span=1):
        self.loadRules(filename)
        start = int(start)
        span = int(span)
        filelen = self.linesJson(filename)
        curLine=0

        newfile = filename[:filename.rfind('/')+1]+"new_"+filename[filename.rfind('/')+1:]
        with open("%s" % filename,"r") as of:
            line= of.readline()
            curLine+=1
            with open("%s" % newfile, "w") as nf:
                nf.write("%s" % line)
                #first we write until we hit the changed lines
                for i in range(0,start-1):
                    line = of.readline()
                    curLine+=1
                    nf.write(line)
                #then we validate the changed lines
                for i in range(0,span):
                    data=json.loads(of.readline().rstrip(",\n"))
                    curLine+=1
                    for i in range(0,len(self.rules)):
                        if(str(self.rules[i])[str(self.rules[i]).find('.')+1:str(self.rules[i]).find('R')])=="dependency":
                            data[self.rules[i].getLabel()]["value"]=str(self.rules[i].validate(data[self.rules[i].getDepends()]["value"]))
                            data[self.rules[i].getLabel()]["validated"]=str(True)
                        else:
                            data[self.rules[i].getLabel()]["validated"]=str(self.rules[i].validate(data[self.rules[i].getLabel()]["value"]))
                    if curLine < filelen-1:
                        nf.write("%s,\n" % str(data).replace("'","\""))
                    else:
                        nf.write("%s\n" % str(data).replace("'","\""))
                # now we write the unchanged rest ...
                while line:
                    line = of.readline()
                    nf.write(line)
        os.remove(filename)
        os.rename(newfile, filename)
