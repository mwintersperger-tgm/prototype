import json

class RuleController():
    def __init__(self):
        #create a dict
        self.rule_data = {"rules":[]}
        # turn it into a list so you can append
        self.data_holder = self.rule_data["rules"]

    def createTextRule(self, label="text",minlength=0,maxlength=100,letters=[]):
        self.data_holder.append({'label':label, "rule":"text", 'minlength':minlength, 'maxlength':maxlength, 'letters':letters})

    def createIdRule(self, label="id"):
        self.data_holder.append({'label':label, "rule":"id"})

    def createNumberRule(self, label="number",lower=-100000,upper=100000):
        self.data_holder.append({'label':label, "rule":"number", 'lower':lower, 'upper':upper})

    def createDateRule(self, label="date", pattern="%d-%m-%Y", separator="/" ):
        self.data_holder.append({'label':label, "rule":"date", 'pattern':pattern, 'separator':separator})

    def createEmailRule(self, label="email", domain="at" ):
        self.data_holder.append({'label':label, "rule":"email", 'domain':domain})

    def createRulesFile(self,name):
        with open(name, 'w') as outfile:
            json.dump(self.rule_data, outfile)
        outfile.close()
