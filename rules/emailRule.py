
class EmailRule():
    def __init__(self, label, domain):
        self.label = label
        self.domain = domain

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
            if value[(len(value)-len(self.domain)):] == self.domain:
                if "@" in value:
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
