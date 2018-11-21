import datetime

class DateRule():
    def __init__(self, label, pattern, separator):
        self.label = label
        self.pattern = pattern
        self.separator = separator

    def validate(self, values):
        list = []
        for i in values:
            try:
                datetime.datetime.strptime(i.replace(self.separator, "-"), self.pattern)
                list.append(True)
            except ValueError:
                list.append(False)
        return list

    def getLabel(self):
        return self.label
