import re

class PatternRule():
    def __init__(self, label, pattern):
        self.label = label
        self.pattern = re.compile(pattern)

    def validate(self, value):
        if self.pattern.match(value) is not None:
            return True
        else:
            return False

    def getLabel(self):
        return self.label
