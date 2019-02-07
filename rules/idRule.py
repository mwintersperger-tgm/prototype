
class IdRule():
    def __init__(self, label, digits):
        self.label = label
        self.digits = int(digits)

    def validate(self, value):
        """
        Adds leading zeroes
        :param value: the value to be added leading zeroes too
        :type: string
        :return: the value iwth added leading zeroes
        :rtype: string
        """
        return str(value).rjust(self.digits, '0')

    def getLabel(self):
        """
        return the label the the data entry this rule applies to
        :return: the label
        :rtype: string
        """
        return self.label
