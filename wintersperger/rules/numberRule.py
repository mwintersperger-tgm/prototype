
class NumberRule():
    def __init__(self, label, upper, lower):
        self.label = label
        self.upper = upper
        self.lower = lower

    def validate(self, value):
        """
        checks if the value follows the rules
        :param value: the value to be checked
        :type: string
        :return: the result of the check
        :rtype: bool
        """
        value = int(value)
        validated = False
        if value > self.lower and value < self.upper:
            validated = True
        return validated

    def getLabel(self):
        """
        return the label the the data entry this rule applies to
        :return: the label
        :rtype: string
        """
        return self.label
