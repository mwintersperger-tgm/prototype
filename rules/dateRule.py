import datetime

class DateRule():
    def __init__(self, label, pattern, separator):
        self.label = label
        self.pattern = pattern
        self.separator = separator

    def validate(self, value):
        value = str(value)
        validated = False
        try:
            datetime.datetime.strptime(value.replace(self.separator, "-"), self.pattern)
            validated = True
        except ValueError:
            validated = False
        return validated

    def getLabel(self):
        return self.label
