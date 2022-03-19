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
activityStatus = "FAILED"


extraArgs = {}
excections = []
x = 0


def writetocsv(stopdate, name, input, status, cause, x):
    filename = stopdate+"_excecutions_"+activityStatus+".csv"
    if x == 1:
        o = open(filename, "w", newline='')
        writer = csv.DictWriter(
            o, fieldnames=["ExcecutionFinishedDate", "ExcecutionName", "Input", "Status", "Error Cause"])
        writer.writeheader()
        o.close()
    f = open(filename, 'a', newline='')
    writer = csv.writer(f)
    entry = [stopdate, name, input, status, cause]
    writer.writerow(entry)
    f.close()


while True:
    response = client.list_executions(
        stateMachineArn=stateMachineArn,
        statusFilter=activityStatus,
        maxResults=1000, **extraArgs)
    excections = response['executions']+excections
    if 'nextToken' in response:
        extraArgs['nextToken'] = response['nextToken']
    else:
        break

for item in excections:
    executionName = item['name']
    stopdatets = item['stopDate']
    stopDate = stopdatets.strftime('%Y-%m-%d')
    status = item['status']
    todayDate = (datetime.datetime.today() -
                 datetime.timedelta(days=0)).strftime('%Y-%m-%d')
    if stopDate == todayDate:
        executionArn = executionArnprefix+":"+executionName
        response = client.describe_execution(executionArn=executionArn)
        print(response['input'])
        input = json.loads(response['input'])
        execution_history = client.get_execution_history(executionArn=executionArn,
                                                         maxResults=1,
                                                         reverseOrder=True,
                                                         includeExecutionData=True
                                                         )
        cause = ""
        if 'executionFailedEventDetails' in execution_history['events'][0].keys():
            cause = str(
                execution_history['events'][0]['executionFailedEventDetails']['cause'])
            print(cause)
        x = x+1
        writetocsv(stopDate, executionName, input, status, cause, x)

print("Number of excecutions failed on "+todayDate+":"+str(x))
