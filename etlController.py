from rules.textRule import TextRule
from rules.numberRule import NumberRule
from rules.emailRule import EmailRule
from rules.dateRule import DateRule
from rules.patternRule import PatternRule
from rules.listRule import ListRule
from rules.dependencyRule import DependencyRule
from rules.blankRule import BlankRule

import json
import os


class ETLController:
    """
    This class handles the whole validation process of Datamigration.

    It allows you to change the rule file applied to a data file, change the CC of a data file,
    load the rules applied to a data file and validate data.
    """
    def loadRules(self, filename):
        """
        This functions reads the rules applied to a data file out of the rule file applied to it,
        creates instances of the rule classes and saves them in a list
        :param filename: the name/path of the data file
        :type: string
        :return: void
        """
        self.rules = []
        # get the rule file applied to this data file
        rulename = self.getRule(filename)
        filelen = self.fileLength(rulename)
        with open(rulename, "r") as f:
            f.readline()
            # we ignore the 'header' and the closing line
            for i in range(1, filelen-1):
                rule = json.loads(f.readline().rstrip(",\n"))
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

                elif rule["rule"] == "blank":
                    self.rules.append(BlankRule(str(rule["label"])))

    def setCC(self, filename, cc):
        """
        This function changes the cc of the data file
        :param filename: the name/path of the data file
        :type: string
        :param cc: the new cc of the data file
        :type: string
        :return: void
        """

        # the newfile has the same path as the old one but its name gets a "new_" added to it
        newfile = filename[:filename.rfind('/')+1]+"new_"+filename[filename.rfind('/')+1:]
        filelen = self.fileLength(filename)
        with open("%s" % filename, "r") as of:
            temp = of.readline()
            rule = temp[10:temp.find(",")-1]
            with open("%s" % newfile, "w") as nf:
                # write the header with the new rules
                line = '{"rules":"%s", "cc":"%s", "values":[\n' % (rule, cc)
                nf.write(line)

                # write the rest
                for i in range(1, filelen):
                    line = of.readline()
                    nf.write(line)
        # remove the old file and rename the new file to the old one
        os.remove(filename)
        os.rename(newfile, filename)

    def setRules(self, filename, rule):
        """
        This function changes the rule file applied to a data file
        :param filename: the name/path of the data file
        :type: string
        :param rule: the name/path of the new rule file
        :type: string
        :return: void
        """

        # the newfile has the same path as the old one but its name gets a "new_" added to it
        newfile = filename[:filename.rfind('/')+1]+"new_"+filename[filename.rfind('/')+1:]
        filelen = self.fileLength(filename)
        with open("%s" % filename, "r") as of:
            temp = of.readline()
            cc = temp[temp.find("cc")+5:temp.rfind(",")-1]
            with open("%s" % newfile, "w") as nf:
                # write the header with the new rules
                line = '{"rules":"%s", "cc":"%s", "values":[\n' % (rule, cc)
                nf.write(line)

                # write the rest
                for i in range(1, filelen):
                    line = of.readline()
                    nf.write(line)
        # remove the old file and rename the new file to the old one
        os.remove(filename)
        os.rename(newfile, filename)

    def getRule(self, filename):
        """
        This function reads the first line of a data file and reads the name/path of the rule file applied to it
        :param filename: the name/path of the data file
        :type: string
        :return: the name/path of the rule file applied to the data file
        :rtype: string
        """
        with open("%s" % filename, "r") as f:
            rule = f.readline()
            rule = rule[10:-rule.find("cc")-2]
            return rule

    def fileLength(self, filename):
        """
        This function returns the number of lines in a file
        :param filename: the name/path of the data file
        :type: string
        :return: the number of lines in the file
        :rtype: integer
        """
        num_lines = sum(1 for line in open(filename))
        return num_lines

    def runRules(self, filename, start=0, span=1):
        """
        This function validates data entries in the data file by applying the rules from the rule file defined in the data file.
        :param filename: the name/path of the data file
        :type: string
        :param start: the index of the data entry the method starts to validate
        :type: integet
        :param span:  the number of data entries the method validates
        :type: integer
        :return: void
        """
        self.loadRules(filename)
        start = int(start)
        span = int(span)
        filelen = self.fileLength(filename)
        # if the starting index is higher than possible the index is set to the highest possible index
        if start > filelen - 3:
            start = filelen - 3
        # if the span is longer than possible the span is set to cover the remaining data entries
        if start + span > filelen - 2:
            span = filelen - 2 - start
        # this counter is needed to know when the last data entry is written
        curline = 0

        # the newfile has the same path as the old one but its name gets a "new_" added to it
        newfile = filename[:filename.rfind('/')+1]+"new_"+filename[filename.rfind('/')+1:]
        with open("%s" % filename, "r") as of:
            line = of.readline()
            curline += 1
            with open("%s" % newfile, "w") as nf:
                nf.write("%s" % line)
                # first we write until we hit the changed lines
                for i in range(0, start-1):
                    line = of.readline()
                    curline += 1
                    nf.write(line)
                # then we validate the changed lines
                for i in range(0, span):
                    # strip ',\n' from the lines to use them as dictionaries
                    data = json.loads(of.readline().rstrip(",\n"))
                    curline += 1
                    for j in range(0, len(self.rules)):
                        # dependency rules work different than normal rules so we have to check if the rules is one
                        if(str(self.rules[j])[str(self.rules[j]).find('.')+1:str(self.rules[j]).find('R')]) == "dependency":
                            # set the value of the dependent data entry depending of the value of the value of the data entry this one depends on
                            data[self.rules[j].getLabel()]["value"] = str(self.rules[j].validate(data[self.rules[j].getDepends()]["value"]))
                            # set validated to True or False depending of the dependency validation
                            if data[self.rules[j].getLabel()]["value"] is None:
                                data[self.rules[j].getLabel()]["validated"] = str(False)
                            else:
                                data[self.rules[j].getLabel()]["validated"] = str(True)
                        else:
                            # set the validation of the current data entry
                            data[self.rules[j].getLabel()]["validated"] = str(self.rules[j].validate(data[self.rules[j].getLabel()]["value"]))
                    # add either a ',\n' or a '\' and replace the ' of the dictionary with the " required by json
                    if curline < filelen-1:
                        nf.write("%s,\n" % str(data).replace("'", "\""))
                    else:
                        nf.write("%s\n" % str(data).replace("'", "\""))
                # now we write the unchanged rest ...
                while line:
                    line = of.readline()
                    nf.write(line)
        # remove the old file and rename the new file to the old one
        os.remove(filename)
        os.rename(newfile, filename)
