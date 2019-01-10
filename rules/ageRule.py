from datetime import datetime, date

class AgeRule():
    def __init__(self, label, depends, pattern, separator):
        self.label = label
        self.depends = depends
        self.pattern = pattern
        self.separator = separator

    def validate(self, value):
        """
        tries to calculate the age based on a date
        :param value: the value calcualte the age of
        :type: string
        :return: the result of the calculation
        :rtype: string
        :type: None
        """
        try:
            value = datetime.strptime(value.replace(self.separator, "-"), self.pattern)
            today = date.today()
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            return age
        except:
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
