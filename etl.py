from etlController import ETLController
from ruleController import RuleController
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", help="path to the data file", required=False)
    parser.add_argument("-st","--start", help="from which data number", required=False)
    parser.add_argument("-sp","--span", help="span of data", required=False)

    args = parser.parse_args()
    rules = RuleController()
    rules.createTextRule("firstname",0,100,[ ",", "'"])
    rules.createTextRule("lastname",0,100,[])
    rules.createNumberRule("income",200,5000)
    rules.createDateRule("birthday","%d-%m-%Y","/")
    rules.createEmailRule("email","at")
    rules.createRulesFile("test.json")

    ETL = ETLController()
    ETL.loadRules(args.data)
    ETL.runRules(args.data,args.start,args.span)

if __name__ == '__main__':
    main()
