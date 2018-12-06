import json

class RuleController():
    def __init__(self):
        #create a dict
        self.rule_data = '{"rules":[\n'
        # turn it into a list so you can append

    def createTextRule(self, label="text",minlength=0,maxlength=100,letters=[]):
        self.rule_data+='{"label":"%s", "rule":"text", "minlength":"%s", "maxlength":"%s", "letters":"%s"},\n' %(label,minlength,maxlength,letters)

    def createNumberRule(self, label="number",lower=-100000,upper=100000):
        self.rule_data+='{"label":"%s", "rule":"number", "lower":"%d", "upper":"%d"},\n' % (label,lower,upper)

    def createDateRule(self, label="date", pattern="%d-%m-%Y", separator="/" ):
        self.rule_data+='{"label":"%s", "rule":"date", "pattern":"%s", "separator":"%s"},\n' %(label,pattern,separator)

    def createEmailRule(self, label="email", domain="at" ):
        self.rule_data+='{"label":"%s", "rule":"email", "domain":"%s"},\n' % (label,domain)

    def createListRule(self, label="list", list=[]):
        self.rule_data+='{"label":"%s", "rule":"list", "list":"%s"},\n' % (label,list)

    def createDependencyRule(self, label="dependency", dict={}, depends=""):
        self.rule_data+='{"label":"%s", "rule":"dependency", "dict":%s, "depends":"%s"},\n' %(label,str(dict).replace("'","\""),depends)

    def createRulesFile(self,name):
        self.rule_data = self.rule_data[:len(self.rule_data)-2]+'\n]}'
        with open(name, 'w') as outfile:
            outfile.write(self.rule_data)
        outfile.close()
