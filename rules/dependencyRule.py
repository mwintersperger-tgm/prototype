class DependencyRule():
    def __init__(self, label, dict, depends):
        self.label = label
        self.dict ={}
        self.dict.update(dict)
        self.depends = depends

    def validate(self, value):
        for i in self.dict:
            if value == i:
                return self.dict[i]
        return None

    def getLabel(self):
        return self.label

    def getDepends(self):
        return self.depends
