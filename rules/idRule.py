class IdRule():
    def __init__(self, label):
        self.label = label

    def validate(self, values):
        list = []
        unique_list = []
        for i in values:
            if i not in unique_list:
                unique_list.append(i)
                list.append(True)
            else:
                list.append(False)
        return list

    def getLabel(self):
        return self.label
