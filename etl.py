from etlController import ETLController
from ruleController import RuleController
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", help="path to the data file", required=False)

    args = parser.parse_args()
    rules = RuleController()
    rules.createTextRule("firstname",0,100,[ ",", "'"])
    rules.createTextRule("lastname",0,100,[])
    rules.createNumberRule("income",200,5000)
    rules.createDateRule("birthday","%d-%m-%Y","/")
    rules.createEmailRule("email","at")
    rules.createRulesFile("test.json")

    ETL = ETLController(args.data)


if __name__ == '__main__':
    main()
	pass
