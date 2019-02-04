from etlController import ETLController
from ruleController import RuleController
from userController import UserController
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", help="path to the data file", required=True)
    parser.add_argument("-r", "--rule", help="path to the rule file", required=True)
    parser.add_argument("-st", "--start", help="from which data entry index", required=True)
    parser.add_argument("-sp", "--span", help="span of data entries", required=True)
    parser.add_argument("-cc", "--countrycode", help="the country code of the data file", required=True)

    user = UserController()
    user.addUser("Michael","123Fiona","User","['AU','US']")
    print(user.checkUser("Benjamin","2"))
    user.removeUser("Michael")
"""
    args = parser.parse_args()
    rules = RuleController()
    rules.initRules()
    rules.createTextRule("firstname", 0, 10, ["*"])
    rules.createTextRule("lastname", 0, 10, [])
    rules.createNumberRule("age", 18, 25)
    rules.createListRule("job", ["Programmierer", "Anwalt"])
    rules.createDependencyRule("income", {"Anwalt": 500, "Programmierer": 1000}, "job")
    rules.createDateRule("birthday", "%d-%m-%Y", "-")
    rules.createEmailRule("email", "at")
    rules.createRulesFile(args.rule)

    etl = ETLController()
    etl.setCC(args.data, args.countrycode)
    etl.setRules(args.data, args.rule)
    etl.simpleReplace(args.data, "birthday", {"-": "/"})
    etl.runRules(args.data, args.start, args.span)
"""

if __name__ == '__main__':
    main()
