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
        with open('%s' % self.getRules(data)) as f:
            self.rulesData = json.load(f)
        self.rules = []
        for i in range(len(self.rulesData["rules"])):
            if self.rulesData["rules"][i]["rule"] == "text":
                self.rules.append(TextRule(self.rulesData["rules"][i]["label"], self.rulesData["rules"][i]["minlength"], self.rulesData["rules"][i]["maxlength"], self.rulesData["rules"][i]["letters"]))

            elif self.rulesData["rules"][len(self.rules)]["rule"] == "number":
                self.rules.append(NumberRule(self.rulesData["rules"][i]["label"], self.rulesData["rules"][i]["upper"], self.rulesData["rules"][i]["lower"]))

            elif self.rulesData["rules"][len(self.rules)]["rule"] == "email":
                self.rules.append(EmailRule(self.rulesData["rules"][i]["label"], self.rulesData["rules"][i]["domain"]))

            elif self.rulesData["rules"][len(self.rules)]["rule"] == "date":
                self.rules.append(DateRule(self.rulesData["rules"][i]["label"], self.rulesData["rules"][i]["pattern"], self.rulesData["rules"][i]["separator"]))

            elif self.rulesData["rules"][len(self.rules)]["rule"] == "pattern":
                self.rules.append(PatternRule(self.rulesData["rules"][i]["label"], self.rulesData["rules"][i]["pattern"]))

            elif self.rulesData["rules"][len(self.rules)]["rule"] == "list":
                self.rules.append(ListRule(self.rulesData["rules"][i]["label"], self.rulesData["rules"][i]["list"]))

            elif self.rulesData["rules"][len(self.rules)]["rule"] == "dependency":
                self.rules.append(DependencyRule(self.rulesData["rules"][i]["label"], self.rulesData["rules"][i]["list"], self.rulesData["rules"][i]["offset"]))

    def setRules(self,filename,rule):
        of = open(filename, "r")
        newfile = filename
        nf = open(newfile, "w")
        filelen = self.linesJson(filename)
        line = of.readline()
        nf.write(line)
        newRule = '"rules":"%s",' % rule
        nf.write("	%s\n" % (newRule))
        of.readline()
        done = 0
        while done < filelen-2:
            line = of.readline()
            nf.write(line)
            done += 1
        of.close()
        nf.close()

        #os.remove(filename)
        #os.rename("new_"+filename, filename)

    def getRules(self,filename):
        with open("%s" % filename) as f:
            fileData = json.loads(f.readline())
            print(fileData)

        f = open(filename, "r")
        f.readline()
        raw = f.readline()
        rule = raw[(raw.find(':"')+2):raw.find('",')]
        f.close()
        return rule

    def linesJson(self, filename):
        f = open(filename, "r")
        linenumber = sum(1 for line in f)
        f.close()
        return linenumber

    def runRules(self, filename, begin=0, nval=1):
        begin = int(begin)
        nval = int(nval)
        of = open(filename, "r")
        filelen = self.linesJson(filename)
        # read header ...
        headerlen = 1
        line = of.readline()
        while line.find("[") is -1:
            line = of.readline()
            headerlen += 1
        # read number of values
        valuelen = len(self.rules)
        # with the the { and }, a value contains valulen + 2 lines
        valuelen += 2
        # now we have to read all lines until begin (=first changed value)
        begin_of_change = headerlen + begin * valuelen
        # go back to beginning of source file
        of.seek(0)
        # and write the lines until begin
        # to newfile because they are unchanged ...
        newfile = "new_"+filename
        nf = open(newfile, "w")
        done = 0
        while done < begin_of_change:
            line = of.readline()
            nf.write(line)
            done += 1
        # now we write the changed values instead of the original ones ...
        i = 0
        while i < nval:
            of.readline()
            nf.write("		{\n")
            ll = valuelen - 2
            j = 0
            while j < ll:
                print(str(self.rules[j])[str(self.rules[j]).find('.')+1:str(self.rules[j]).find('R')])
                if (str(self.rules[j])[str(self.rules[j]).find('.')+1:str(self.rules[j]).find('R')] == "dependency"):
                    print(of.tell())
                    of.seek(of.tell()+self.rules[j].getOffset(),1)
                    print(of.tell())
                    rawValue = of.readline()
                    value = rawValue[(rawValue.find('value"')+8):(rawValue.find('"validated')-3)]
                    combinedValue = rawValue[(rawValue.find('"')):(rawValue.find(':'))]+':{"value":"'+str(self.rules[j].validate(value))+'"}'
                    of.seek(of.tell()+self.rules[j].getOffset()*-1,1)
                else:
                    rawValue = of.readline()
                    value = rawValue[(rawValue.find('value"')+8):(rawValue.find('"validated')-3)]
                    combinedValue = rawValue[(rawValue.find('"')):(rawValue.find(':'))]+':{"value":"'+value+'", "validated":"'+str(self.rules[j].validate(value))+'"}'
                if (j < ll-1): combinedValue += ","
                nf.write("			%s\n" % (combinedValue))
                j += 1
                done += 1
            of.readline()
            i += 1
            if done > filelen - 1 - valuelen:  # could be last value ...
                nf.write("		}\n")
            else:
                nf.write("		},\n")
            done += 3
        line = of.readline()
        # now we write the unchanged rest ...
        while line:
            nf.write(line)
            line = of.readline()
            done += 1
        of.close()
        nf.close()

        #os.remove(filename)
        #os.rename("new_"+filename, filename)
