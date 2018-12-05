import re

class PatternRule():
    def __init__(self, label, pattern):
        self.label = label
        self.pattern = re.compile(pattern)

    def validate(self, value):
        validated = False
        if self.pattern.match(value) is not None:
            validated = True
        return validated

    def getLabel(self):
        return self.label
