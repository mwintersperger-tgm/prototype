
class ListRule():
    def __init__(self, label, list):
        self.label = label
        self.list = list.replace("[","").replace("'","").replace("]","").split(",")

    def validate(self, value):
        """
        checks if the value follows the rules
        :param value: the value to be checked
        :type: string
        :return: the result of the check
        :rtype: bool
        """
        validated = False
        for i in self.list:
            if value == i:
                validated = True
        return validated

    def getLabel(self):
        """
        return the label the the data entry this rule applies to
        :return: the label
        :rtype: string
        """
        return self.label
