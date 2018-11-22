from etlController import ETLController
from ruleController import RuleController
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", help="path to the data file", required=True)
    parser.add_argument("-st","--start", help="from which data number", required=True)
    parser.add_argument("-sp","--span", help="span of data", required=True)
    parser.add_argument("-r","--rule", help="path to the rule file", required=True)

    args = parser.parse_args()
    rules = RuleController()
    rules.createTextRule("firstname",0,100,[ ",", "'"])
    rules.createTextRule("lastname",0,15,[])
    rules.createNumberRule("age",14,22)
    rules.createDateRule("birthday","%d-%m-%Y","/")
    rules.createEmailRule("email","at")
    rules.createListRule("job",["Programmierer","Anwalt"])
    rules.createDependencyRule("income",["Programmierer","Anwalt"],-1)
    rules.createRulesFile(args.rule)

    ETL = ETLController()
    ETL.setRules(args.data, args.rule)
    ETL.loadRules(args.data)
    ETL.runRules(args.data,args.start,args.span)

if __name__ == '__main__':
    main()
