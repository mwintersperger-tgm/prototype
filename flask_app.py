from flask import Flask, jsonify, request, render_template_string
import json
from collections import OrderedDict
from flask_cors import CORS

from datetime import datetime

import ruleController
from importPkg import importCls
from etlController import ETLController
from exportPkg import exportCls
# import jinja2
import os
# from os import listdir, fspath
# from os.path import isfile, join
import sys
# dirname = os.path.dirname("C:/Users/tschwede´r/Documents/Incomedia/WebSite X5 - Evolution/xXx/Preview")
# filename = os.path.join(dirname, '/Preview')
# enable CORS



app = Flask(__name__)

CORS(app)
# app.jinja_loader = jinja2.FileSystemLoader('../Preview')

def logger(action = "action", user = "musterman"):
    with open("log.txt","rw") as log:
        log.seek(0)
        log.write("User: %s, Action: %s, Date: %s\n" %(user,action,datetime.now()))

@app.route('/')
def hello_rasic():
    # onlyfiles = [f for f in listdir(os.fspath("../Preview")) if isfile(join(os.fspath("../Preview"), f))]
    importCls.importcsv('datacsv.csv', 'data.json', '|')
    """temp = {}
	with open('exportPkg/data_backup_v2.json') as file:
		temp = json.load(file)

	exportCls.exportCSV(temp['values'], 'datacsv.csv')"""
    # html = open("../import.html").read()
    # print(template_folder)
    logger("Import file: %s" % "file", "user")
    return 'done'


# return 'Hello, World!'
@app.route('/rules',methods=['GET', 'POST'])
def createRules():
    rc = ruleController()
    rc.initRules()
    ruleType = request.args["ruleType"]
    label = request.args["label"]
    if(ruleType=="text"):
        minlength = request.args["minlength"]
        maxlength = request.args["maxlength"]
        letters = request.args["letters"]
        rc.createTextRule(label,minlength,maxlength,letters)
    elif(ruleType=="number"):
        lower = request.args["lower"]
        upper= request.args["upper"]
        rc.createNumberRule(label,lower,upper)
    elif(ruleType=="date"):
        pattern = request.args["pattern"]
        seperator = request.args["seperator"]
        rc.createDateRule(label,pattern,seperator)
    elif(ruleType=="email"):
        domain = request.args["domain"]
        rc.createEmailRule(label,domain)
    elif(ruleType=="list"):
        list = request.args["list"]
        rc.createListRule(label,list)
    elif(ruleType=="dependency"):
        dict = request.args["key"]
        depends = request.args["depending"]
        rc.createDependencyRule(label,dict,depends)
    elif(ruleType=="age"):
        depends = request.args["ageDepends"]
        pattern = request.args["agePattern"]
        seperator = request.args["ageSpeerator"]
        rc.createAgeRule(label,depends,pattern,seperator)
    else:
        print("Sumting went wong!")


    rc.createRulesFile("newRule.json")
    logger("Created rules file: %s" % "file", "user")



@app.route('/validate')
def validateExe():
    etl = ETLController()
    etl.setRules('data.json', 'rule.json')
    etl.runRules('data.json', 0, 100)
    logger("Validated file: %s from %i to %i" % ("file",0,100), "user")
    return 'done validate'

@app.route('/g', methods=['GET'])
def hello_world():
    #simple get methode for json data
    json_data=open('data.json').read()
    ftable = json.loads(json_data)
    FIRSTTABLE = ftable
    return jsonify(FIRSTTABLE)

@app.route('/post', methods=['POST'])
def postData():
    response_object = {'status': 'success'}
    data = request.get_json()
    #grab data
    d = data["data"]["data"]

    ordList = []
    order = ["firstname","lastname","age","job","income","birthday","email"]
    #order the values as specified above
    for z in range(len(data["data"]["data"])):
        ordList.insert(z,OrderedDict((k,d[z][k]) for k in order))
    TEST = {"rules":"rule.json","cc":"EN","values":[]}
    TEST["values"].extend(ordList)

    #overwrite data.json
    with open('data.json', 'w') as outfile:
        #write first line as needed
        outfile.write('{"rules":"rule.json", "cc":"EN", "values":[ \n')
        #write values as json with , as needed
        for m in range(len(TEST["values"])):
            if(m<len(TEST["values"])-1):
                outfile.write("%s,\n" % json.dumps(TEST["values"][m]))
            else:
                outfile.write("%s\n" % json.dumps(TEST["values"][m]))
        #write last line
        outfile.write("]}")
    logger("Edited File: %s" % "file", "user")
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
