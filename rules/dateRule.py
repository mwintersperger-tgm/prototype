import datetime

class DateRule():
    def __init__(self, label, pattern, separator):
        self.label = label
        self.pattern = pattern
        self.separator = separator

    def validate(self, value):
        try:
            datetime.datetime.strptime(value.replace(self.separator, "-"), self.pattern)
            return True
        except ValueError:
            return False

    def getLabel(self):
        return self.label
