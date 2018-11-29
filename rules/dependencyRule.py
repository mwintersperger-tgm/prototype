class DependencyRule():
    def __init__(self, label, list, depends):
        self.label = label
        self.list = list
        self.depends = depends

    def validate(self, value):
        for i in self.list:
            if value == i:
                return i

    def getLabel(self):
        return self.label

    def getDepends(self):
        return self.depends
