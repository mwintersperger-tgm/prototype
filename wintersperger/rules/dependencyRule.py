
class DependencyRule():
    def __init__(self, label, dict, depends):
        self.label = label
        self.dict ={}
        self.dict.update(dict)
        self.depends = depends

    def validate(self, value):
        """
        checks if the value can be found in the list
        :param value: the value to be checked
        :type: string
        :return: the result of the check
        :rtype: string
        :type: None
        """
        for i in self.dict:
            if value == i:
                return self.dict[i]
        return None

    def getLabel(self):
        """
        return the label the the data entry this rule applies to
        :return: the label
        :rtype: string
        """
        return self.label

    def getDepends(self):
        """
        return the label the the data entry this rule depends on
        :return: the label
        :rtype: string
        """
        return self.depends
