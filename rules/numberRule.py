class NumberRule():
    def __init__(self, label, upper, lower):
        self.label = label
        self.upper = upper
        self.lower = lower

    def validate(self, value):
        value = int(value)
        validated = False
        if value > self.lower and value < self.upper:
            validated = True
        return validated

    def getLabel(self):
        return self.label
