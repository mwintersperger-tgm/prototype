
class TextRule():
    def __init__(self, label, minlength, maxlength, letters):
        self.label = label
        self.minlength = minlength
        self.maxlength = maxlength
        self.letters = letters

    def validate(self, value):
        """
        checks if the value follows the rules
        :param value: the value to be checked
        :type: string
        :return: the result of the check
        :rtype: bool
        """
        validated = False
        try:
            value = str(value)
            if len(value) < self.maxlength+1 and len(value) > self.minlength-1:
                validated = True
            for j in self.letters:
                if j in value:
                    validated = False
            return validated
        except:
            return validated

    def getLabel(self):
        """
        return the label the the data entry this rule applies to
        :return: the label
        :rtype: string
        """
        return self.label
