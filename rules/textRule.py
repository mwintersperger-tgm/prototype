class TextRule():
    def __init__(self, label, minlength, maxlength, letters):
        self.label = label
        self.minlength = minlength
        self.maxlength = maxlength
        self.letters = letters

    def validate(self, value):
        value = str(value)
        validated = False
        if len(value) < self.maxlength+1 and len(value) > self.minlength-1:
            validated = True
        for j in self.letters:
            if j in value:
                validated = False
        return validated

    def getLabel(self):
        return self.label
