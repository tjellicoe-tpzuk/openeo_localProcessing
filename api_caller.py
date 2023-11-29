import os
import requests
import json
import time

import urllib3
urllib3.disable_warnings() ## temporary fix only!

base = "https://"
domain = "192-168-49-2.nip.io"
ades = f"ades-open.{domain}"
login = f"auth.{domain}"
user = "eric"
passW = "defaultPWD"
clientId = "6195909b-04bc-4d8c-8b92-9cb4e1bdea1f"
clientSecret = "9a614fe9-b1eb-465d-a0af-85115dcba2e6"

### Complete these lines as required to test the desired files
cwlLocation = "https://raw.githubusercontent.com/EOEPCA/deployment-guide/main/deploy/samples/requests/processing/snuggs.cwl"
cwlScriptName = "snuggs-0_3_0"
inputDataLocation = "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/S2A_38VNM_20221124_0_L2A"
inputSExpression = "ndvi:(/ (- B05 B03) (+ B05 B03))"
######

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def listProcesses():
    ### List processes
    apiQuestion = base + ades + "/" + user + "/wps3/processes"

    print(apiQuestion)

    apiHeader = {'Accept': 'application/json'}

    rawAnswer = requests.get(apiQuestion, headers=apiHeader, verify=False) #verify False due to issue here: https://support.chainstack.com/hc/en-us/articles/9117198436249-Common-SSL-Issues-on-Python-and-How-to-Fix-it

    return rawAnswer

    print(json.dumps(rawAnswer.json(), indent=4))

def deployProcess():
    ### Deploy Process
    

    apiQuestion = base + ades + "/" + user + "/wps3/processes"

    apiHeader = {'Accept': 'application/json',
                'Content-Type': 'application/json'}

    apiParams = {
        "executionUnit": {
            "href": f"{cwlLocation}",
            "type": "application/cwl"
        }
    }

    rawAnswer = requests.post(apiQuestion, headers=apiHeader, verify=False, json=apiParams) #verify False due to issue here: https://support.chainstack.com/hc/en-us/articles/9117198436249-Common-SSL-Issues-on-Python-and-How-to-Fix-it

    print(rawAnswer.headers)

    return rawAnswer

    print(json.dumps(rawAnswer.json(), indent=4))

def getDeployStatus(deployStatus):
    ### Get Deploy Status

    apiQuestion = base + ades + deployStatus

    apiHeader = {'Accept': 'application/json'}

    rawAnswer = requests.get(apiQuestion, headers=apiHeader, verify=False) #verify False due to issue here: https://support.chainstack.com/hc/en-us/articles/9117198436249-Common-SSL-Issues-on-Python-and-How-to-Fix-it

    return rawAnswer

    print(json.dumps(rawAnswer.json(), indent=4))

def executeProcess():
    ### Get Execute Status

    

    apiQuestion = base + ades + "/" + user + "/wps3/processes/" + cwlScriptName + "/execution"

    apiHeader = {'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Prefer': 'respond-async'}
    
    apiParams = {
        "inputs": {
            "input_reference": inputDataLocation,
            "s_expression": inputSExpression
        },
        'response': 'raw'
    }

    rawAnswer = requests.post(apiQuestion, headers=apiHeader, verify=False, json=apiParams) #verify False due to issue here: https://support.chainstack.com/hc/en-us/articles/9117198436249-Common-SSL-Issues-on-Python-and-How-to-Fix-it

    return rawAnswer

    print(json.dumps(rawAnswer.json(), indent=4))


def getExecuteStatus(executeStatus):
    ### Get Execute Status
    apiQuestion = base + ades + executeStatus

    apiHeader = {'Accept': 'application/json'}

    rawAnswer = requests.get(apiQuestion, headers=apiHeader, verify=False) #verify False due to issue here: https://support.chainstack.com/hc/en-us/articles/9117198436249-Common-SSL-Issues-on-Python-and-How-to-Fix-it

    return rawAnswer

    print(json.dumps(rawAnswer.json(), indent=4))


listProcesses()

deployStatus = deployProcess().headers['Location']

getDeployStatus(deployStatus)

executeStatus = executeProcess().headers['Location']

status = getExecuteStatus(executeStatus).json()['status']

while status == "running":
    time.sleep(10)
    status = getExecuteStatus(executeStatus).json()['status']
    print(status)

if status == "successful":
    print(bcolors.OKGREEN + "SUCCESS" + bcolors.ENDC)

if status == "failed":
    print(bcolors.WARNING + "FAILED" + bcolors.ENDC)