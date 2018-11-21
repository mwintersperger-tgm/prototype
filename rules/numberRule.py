class NumberRule():
    def __init__(self, label, upper, lower):
        self.label = label
        self.upper = upper
        self.lower = lower

    def validate(self, values):
        list = []
        for i in values:
            if i > self.lower and i < self.upper:
                list.append(True)
            else:
                list.append(False)
        return list

    def getLabel(self):
        return self.label
