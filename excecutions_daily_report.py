import os
import boto3
import datetime
import csv
import sys
import json
import configparser


client = boto3.client('stepfunctions')
config_parser = configparser.ConfigParser()
config_parser.read('config.ini')
configs = config_parser['config']

extraArgs = {}
excections = []
account =  configs['account_id']
region=configs['region']
orchestrator_name=configs['orchestrator_name']
os.environ['AWS_DEFAULT_REGION'] =  region
stateMachineArn='arn:aws:states:'+region+':'+account+':stateMachine:'+orchestrator_name
executionArnprefix=stateMachineArn.replace("stateMachine", "execution")

todayDate1 = (datetime.datetime.today() -
                 datetime.timedelta(days=0)).strftime('%Y-%m-%d')
print(todayDate1)

def writetocsv(startDate,name, filepath, status, x):
    if x == 1:
        o = open(startDate+"_excecutions.csv", "w", newline='')
        writer = csv.DictWriter(
            o, fieldnames=["StartDate", "excecutionName", "input", "status"])
        writer.writeheader()
        o.close()
    f = open(startDate+"_excecutions.csv", 'a', newline='')
    writer = csv.writer(f)
    entry = [startDate, name, filepath, status]
    writer.writerow(entry)
    f.close()

while True:
    response = client.list_executions(
        stateMachineArn=stateMachineArn,
        maxResults=1000, **extraArgs)
    excections = response['executions']+excections
    if 'nextToken' in response:
        extraArgs['nextToken'] = response['nextToken']
    else:
        break
x = 0
print("Total Number of excections:"+str(len(excections)))

for item in excections:
    executionName = item['name']
    startdatets = item['startDate']
    startDate = startdatets.strftime('%Y-%m-%d')
    startdatets = item['startDate']
    status = item['status']
    todayDate = (datetime.datetime.today() -
                 datetime.timedelta(days=0)).strftime('%Y-%m-%d')
    print(todayDate)
    if(startDate == todayDate):
       executionArn = executionArnprefix+":"+executionName
       response = client.describe_execution(executionArn=executionArn)
       input = json.loads(response['input'])
       #print(input)
       x = x+1
       writetocsv(startDate,executionName, input, status, x)

print("Total Number of excections on "+startDate+":"+str(x))
