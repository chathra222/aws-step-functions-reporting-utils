# AWS Step functions Reporting Utility

## Overview
These scripts can be used to generate daily CSV reports of your step function executions.
When you running thousands of excecutions per day and if you want to know the status of your executions,checking from AWS Management console will not be a good option.Therefore I created these script so its easier to extract overall status of the step function executions.You can run these scripts as cron jobs so daily reports will be ready.;-)

### Configure
First you have to replace following with your own values in config.ini file.
```
account_id = <your aws account id>
region = <your aws region>
orchestrator_name = <your Step function orchestrator name>
```

## Run
1) ``` excecutions_daily_report.py ```
   This script will retrieve the details of all executions that executed today(excecution start date=excecutions_daily_report script running date), including it's excecutionName,status and input.

2) ```failed_excecution_daily_report.py```
   This script retrieve all details of failed excecutions that stopped today(
excecution start date=failed_excecution_daily_report script execution date)
   This will generate a csv file with following fields:
   - "ExcecutionFinishedDate"
   - "ExcecutionName"
   - "Input" 
   - "Status"
   - "Error Cause"
