import datetime

class DateRule():
    def __init__(self, label, pattern, separator):
        self.label = label
        self.pattern = pattern
        self.separator = separator

    def validate(self, value):
        """
        checks if the value follows the rules
        :param value: the value to be checked
        :type: string
        :return: the result of the check
        :rtype: bool
        """
        validated = False
        value = str(value)
        try:
            datetime.datetime.strptime(value.replace(self.separator, "-"), self.pattern)
            validated = True
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
