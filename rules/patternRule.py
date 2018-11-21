import re

class PatternRule():
    def __init__(self, label, pattern):
        self.label = label
        self.pattern = re.compile(pattern)

    def validate(self, values):
        list = []
        for i in values:
            if self.pattern.match(i) is not None:
                list.append(True)
            else:
                list.append(False)
        return list

    def getLabel(self):
        return self.label
