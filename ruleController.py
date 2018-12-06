

class RuleController:

    def initRules(self):
        """
        This function creates/resets the String the other functions append to
        :return: void
        """
        # create the 'header' of the file
        self.rule_data = '{"rules":[\n'

    def createTextRule(self, label="text", minlength=0, maxlength=100, letters=[]):
        """
        This function appends a line defining a textRule to the list
        :param label: the label of the data entry this rule applies to
        :type: string
        :param minlength: the minimum number of characters the data entry has to have
        :type: integer
        :param maxlength: the maximum number of characters the data entry has to have
        :type: integer
        :param letters: a list of letters the data entry is not allowed to contain
        :type: list
        :return: void
        """
        self.rule_data += '{"label":"%s", "rule":"text", "minlength":"%s", "maxlength":"%s", "letters":"%s"},\n' %(label,minlength,maxlength,letters)

    def createNumberRule(self, label="number", lower=-100000, upper=100000):
        """
        This function appends a line defining a numberRule to the list
        :param label: the label of the data entry this rule applies to
        :type: string
        :param lower: the lower bound of the number range the data entry has to be in
        :type: integer
        :param upper: the upper bound of the number range the data entry has to be in
        :type: integer
        :return: void
        """
        self.rule_data += '{"label":"%s", "rule":"number", "lower":"%d", "upper":"%d"},\n' % (label, lower, upper)

    def createDateRule(self, label="date", pattern="%d-%m-%Y", separator="/" ):
        """
        This function appends a line defining a dateRule to the list
        :param label: the label of the data entry this rule applies to
        :type: string
        :param pattern: the pattern the data entry has to follow
        :type: string
        :param separator: the character used to seperate the values
        :type: string
        :return: void
        """
        self.rule_data += '{"label":"%s", "rule":"date", "pattern":"%s", "separator":"%s"},\n' %(label, pattern, separator)

    def createEmailRule(self, label="email", domain="at"):
        """
        This function appends a line defining a emailRule to the list
        :param label: the label of the data entry this rule applies to
        :type: string
        :param domain: the domain the email must have
        :type: string
        :return: void
        """
        self.rule_data += '{"label":"%s", "rule":"email", "domain":"%s"},\n' % (label, domain)

    def createListRule(self, label="list", list=[]):
        """
        This function appends a line defining a listRule to the list
        :param label: the label of the data entry this rule applies to
        :type: string
        :param list: a list of valid strings the data entry can be
        :type: string
        :return: void
        """
        self.rule_data += '{"label":"%s", "rule":"list", "list":"%s"},\n' % (label, list)

    def createDependencyRule(self, label="dependency", dict={}, depends=""):
        """
        This function appends a line defining a dependencyRule to the list
        :param label: the label of the data entry this rule applies to
        :type: string
        :param dict: the key-value list this rule appliess to the data entry
        :type: dictionary
        :param depends: the label of the entry this entry depends on
        :type: string
        :return: void
        """
        self.rule_data += '{"label":"%s", "rule":"dependency", "dict":%s, "depends":"%s"},\n' %(label,str(dict).replace("'","\""), depends)

    def createBlankRule(self, label="blank"):
        """
        This function appends a line defining a blankRule to the list
        :param label: the label of the data entry this rule applies to
        :type: string
        :return: void
        """
        self.rule_data += '{"label":"%s", "rule":"blank"},\n' % label

    def createRulesFile(self, rulename):
        """
        This function persists the rules by writing them into a file
        :param rulename: the label/path of the new rule file
        :type: string
        :return: void
        """
        # remove the '},' of the last added rules and add the proper end of the file
        self.rule_data = self.rule_data[:len(self.rule_data)-2]+'\n]}'
        with open(rulename, 'w') as outfile:
            outfile.write(self.rule_data)
        outfile.close()
