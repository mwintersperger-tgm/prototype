

class ListRule():
    def __init__(self, label, list):
        self.label = label
        self.list = list

    def validate(self, value):
        for i in self.list:
            if value == i:
                return True
        return  False

    def getLabel(self):
        return self.label
