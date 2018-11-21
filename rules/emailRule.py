class EmailRule():
    def __init__(self, label, domain):
        self.label = label
        self.domain = domain

    def validate(self, values):
        list = []
        for i in values:
            if i[(len(i)-len(self.domain)):] == self.domain:
                if "@" in i:
                    list.append(True)
                else:
                    list.append(False)
            else:
                list.append(False)
        return list

    def getLabel(self):
        return self.label
