class NumberRule():
    def __init__(self, label, upper, lower):
        self.label = label
        self.upper = upper
        self.lower = lower

    def validate(self, value):
        if int(value) > self.lower and int(value) < self.upper:
            return True
        else:
            return False

    def getLabel(self):
        return self.label
