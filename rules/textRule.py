class TextRule():
    def __init__(self, label, minlength, maxlength, letters):
        self.label = label
        self.minlength = minlength
        self.maxlength = maxlength
        self.letters = letters

    def validate(self, values):
        list = []
        contains = True
        for i in values:
            if len(i) > self.maxlength and len(i) < self.minlength:
                list.append(False)
            else:
                for j in self.letters:
                    if j in i:
                        contains = False
                    else:
                        contains = True
                if contains:
                    list.append(True)
                else:
                    list.append(False)
        return list

    def getLabel(self):
        return self.label
