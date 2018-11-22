class TextRule():
    def __init__(self, label, minlength, maxlength, letters):
        self.label = label
        self.minlength = minlength
        self.maxlength = maxlength
        self.letters = letters

    def validate(self, value):
        if len(value) < self.maxlength and len(value) > self.minlength:
            for j in self.letters:
                if j in value:
                    return False
            return True
        else:
            return False

    def getLabel(self):
        return self.label
