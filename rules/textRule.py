class TextRule():
    def __init__(self, label, minlength, maxlength, letters):
        self.label = label
        self.minlength = minlength
        self.maxlength = maxlength
        self.letters = letters

    def validate(self, value):
        contains = True
        if len(value) > self.maxlength and len(value) < self.minlength:
            list.append(False)
        else:
            for j in self.letters:
                if j in value:
                    contains = False
                else:
                    contains = True
            if contains:
                return True
            else:
                return False

    def getLabel(self):
        return self.label
