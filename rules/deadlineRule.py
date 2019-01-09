from datetime import datetime, date

class DeadlineRule():
    def __init__(self, label, depends, pattern, separator):
        self.label = label
        self.depends = depends
        self.pattern = pattern
        self.separator = separator

    def validate(self, value):
        """
        tries to calculate number of days until the deadline
        :param value: the value calcualte the age of
        :type: string
        :return: the result of the calculation
        :rtype: string
        :type: None
        """
        try:
            value = datetime.strptime(value.replace(self.separator, "-"), self.pattern)
            today = datetime.today()
            deadline = str(value - today)
            return (deadline[:deadline.find(',')])
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
