# oa2svcnow
Easy python script that exports devices from OpenAudIT to ServiceNow

Overview

Some OpenAudIT users may want to export their device list to ServiceNow.  
We'd like to present an easy python3 script that facilitates the exporting of OpenAudIT devices to ServiceNow.  
This script will work with any ServiceNow schema, simply edit the columnTranslate dictionary found inside and supply the ServiceNow table name in the system variables file.

Prerequisites
- Install the pysnow python module.  http://pysnow.readthedocs.io/en/latest/
- Select a ServiceNow table. (For the uninitiated the table name is not the label presented to humans; it may be found in 'System Definitions - Tables'.)
- Create a mapping of OpenAudIT device attributes to ServiceNow columns. (Again the column name is not the label value.)
- Create a plain text file with server and user attributes.

OpenAudIT Device List

For this exercise we'll want to download the OpenAudIT device list in JSON format.  
This format is the easiest way to convert the device list into a data structure that can be sent to ServiceNow.  
Open a browser to http://<OpenAudIT_server>/omk/open-audit/devices.json.  Some browsers will render the JSON file by default.  
We are interested in the 'attributes' section that each device will have. 

Example:

attributes   
   system.id    "3"
   system.icon    "centos"
   system.ip    "192.168.88.8"
   system.status    "production"
   system.manufacturer    "VMware, Inc."
   system.domain    "opmantek.com"
   system.type    "computer"
   system.name    "thor"
   system.ip_padded    "192.168.088.008"
   system.description    "Linux thor.opmantek.com 2.6.32-696.20.1.el6.x86_64 #1 SMP Fri Jan 26 17:51:45 UTC 2018 x86_64"
   system.os_family    "CentOS"

Attribute Mapping

We need to choose which OpenAudIT attribute will be associated with which ServiceNow column.  
Once this is done update the columnTranslate dictionary in the export script.

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

System Variables

In order for the export script to function it will need usernames, passwords and server information.  
Create a plain text file in the following format with the necessary information.  
When the export script is run it will prompt the user for the file name.

Example:

oaServer:nmis.local
oaUsername:nmis
oaPassword:nm1888
svcnowUsername:admin
svcnowPassword:superSecret
svcnowInstance:1234567
svcnowTable:u_oa
