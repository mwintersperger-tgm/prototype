from etlController import ETLController
from ruleController import RuleController
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", help="path to the data file", required=True)
    parser.add_argument("-r","--rule", help="path to the rule file", required=True)
    parser.add_argument("-st","--start", help="from which data number", required=True)
    parser.add_argument("-sp","--span", help="span of data", required=True)

    args = parser.parse_args()
    rules = RuleController()
    rules.createTextRule("firstname",0,10,["*"])
    rules.createTextRule("lastname",0,10,[])
    rules.createNumberRule("age",18,25)
    rules.createListRule("job",["Programmierer","Anwalt"])
    rules.createDependencyRule("income",{"Anwalt":500,"Programmierer":1000},"job")
    rules.createDateRule("birthday", "%d-%m-%Y", "-" )
    rules.createEmailRule("email", "at" )
    rules.createRulesFile(args.rule)

    ETL = ETLController()
    ETL.setRules(args.data, args.rule)
    ETL.runRules(args.data,args.start,args.span)

if __name__ == '__main__':
    main()
