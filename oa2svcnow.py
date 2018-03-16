#!/usr/bin/python3

### This script will do the following:
### - Log into OpenAudIT and download the device list.
### - Add each device to ServiceNow.

### Import modules
### - requests: For the http transaction with OpenAudIT.
### - json: Convert the OpenAudIT device json file into a python data structure.
### - pysnow: Greatly simplifies the ServiceNow interaction

import requests, json, pysnow

print()
print("""
This script will do the following:
- Log into OpenAudIT and download the device list.
- Add each device to ServiceNow.

The script requires system variables in order to proceed.  Place the variables in a plain text file in the following format:

oaServer:nmis.local
oaUsername:nmis
oaPassword:nm1888
svcnowUsername:admin
svcnowPassword:superSecret
svcnowInstance:1234567
svcnowTable:u_oa 
""")

### Get system variables file.
varFile = input('Enter the full path for systems variables file: ')

### Parse system variables.
varDict = {}
varFileHandle = open(varFile, 'r')
varList = varFileHandle.readlines()
varFileHandle.close()
for i in varList:
    varDict[i.split(':')[0]] = i.split(':')[1].strip()

### This dictionary will be used to translate OpenAudIT columns to ServiceNow columns.  
### Edit this dictionary to suit your needs.
columnTranslate = {
    'system.ip': 'u_ip',
    'system.icon': 'u_icon',
    'system.ip_padded': 'u_ip_padded',
    'system.type': 'u_type',
    'system.manufacturer': 'u_manufacturer',
    'system.name': 'u_name',
    'system.domain': 'u_domain',
    'system.id': 'u_oa_id',
    'system.os_family': 'u_os_family',
    'system.description': 'u_description',
    'system.status': 'u_status'
}

### Create a session to OpenAudIT and download the device list.
oaSession = requests.Session()
print()
print('Logging into OpenAudIT...')
oaSession.post('http://' + varDict['oaServer'] + '/omk/open-audit/login', data = {'username':varDict['oaUsername'], 'password':varDict['oaPassword']})
print('Downloading device data from OpenAudIT...')
oaData = oaSession.get('http://' + varDict['oaServer'] + '/omk/open-audit/devices.json')

### Convert the device list into a data strucutre python can manipulate.
jsonData = json.loads(oaData.text)
oaDataList = jsonData['data']

### Set ServiceNow session attributes
svcnowSession = pysnow.Client(instance = varDict['svcnowInstance'], user = varDict['svcnowUsername'], password = varDict['svcnowPassword'])
svcnowPath =  svcnowSession.resource(api_path = ('/table/' + varDict['svcnowTable']))

### Loop through the device list data strucutre, translate column names, push each device to ServiceNow
print('Pushing data to svcnow...')
for i in oaDataList:
    tempDict = {}
    for k in columnTranslate:
        try:
            tempDict[columnTranslate[k]] = i['attributes'][k]
        except:
            print("##################################################")
            print('OpenAudIT Device #' + i['attributes']['system.id'] + " Did not have " + k)
            print("##################################################")
            pass
    print('Pushing OpenAudIT device #' + tempDict['u_oa_id'] + ' to ServiceNow...')
    svcnowPath.create(payload = tempDict)

### All the devices should now be visable in the appropriate ServiceNow table.
print('This action is complete!')
print()
