import re

class PatternRule():
    def __init__(self, label, pattern):
        self.label = label
        self.pattern = re.compile(pattern)

    def validate(self, value):
        """
        checks if the value follows the rules
        :param value: the value to be checked
        :type: string
        :return: the result of the check
        :rtype: bool
        """
        validated = False
        if self.pattern.match(value) is not None:
            validated = True
        return validated

    def getLabel(self):
        """
        return the label the the data entry this rule applies to
        :return: the label
        :rtype: string
        """
        return self.label
