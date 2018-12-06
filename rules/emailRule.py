class EmailRule():
    def __init__(self, label, domain):
        self.label = label
        self.domain = domain

    def validate(self, value):
        value = str(value)
        validated = False
        if value[(len(value)-len(self.domain)):] == self.domain:
            if "@" in value:
                validated = True
        return validated

    def getLabel(self):
        return self.label
