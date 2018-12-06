class ListRule():
    def __init__(self, label, list):
        self.label = label
        self.list = list.replace("[","").replace("'","").replace("]","").split(",")

    def validate(self, value):
        validated = False
        for i in self.list:
            if value == i:
                validated = True
        return validated

    def getLabel(self):
        return self.label
