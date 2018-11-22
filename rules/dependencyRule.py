class DependencyRule():
    def __init__(self, label, list, offset):
        self.label = label
        self.list = list
        self.offset = offset

    def validate(self, value):
        for i in self.list:
            if value == i:
                return i

    def getLabel(self):
        return self.label

    def getOffset(self):
        return  self.offset
