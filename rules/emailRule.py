class EmailRule():
    def __init__(self, label, domain):
        self.label = label
        self.domain = domain

    def validate(self, value):
        if value[(len(value)-len(self.domain)):] == self.domain:
            if "@" in value:
                return True
            else:
                return False
        else:
            return False

    def getLabel(self):
        return self.label
