from configparser import ConfigParser
import requests, json,os
# Samanage_put.py
# Get variables from samconfig.ini
config = ConfigParser()
config.read('samconfig.ini')
samanage = config['samanage']
fmx = config['fmx']
fmxGet = fmx['fmx_get_url']
fmxUser = fmx['fmxUser']
fmxPass = fmx['fmxPass']

# Hard coded variables
headers = {'Accept':'application/json','Content-Type':'application/json'}
get_equip_url = fmxGet
samanage_key = samanage['samanage_key']
samanage_url = samanage['samanage_url']
samanage_headers = {"X-Samanage-Authorization": samanage_key,"Accept": "application/vnd.samanage.v2.1+json"}
samUrlBase = samanage['samUrlBase']

def fmxUpdate(source,destId):
    #Unpack the source dictionary and use it to form the JSON 
    samIp = source.get('ip')
    samMan = source.get('manufacturer')
    samMod = source.get("model")
    samOs = source.get('os')
    samSerial = source.get('serial')
    samMac = source.get('mac')
    samTag = source.get('tag')
    samUrl = source.get('url')
    samName = source.get('name')
    destUrl = fmx['fmxPostUrl'] + str(destId)
    fmxJson = json.dumps({'customFields': [
        {
            'customFieldID': 318419,
            'name': 'Frederic County Asset Tag',
            'value': samTag
            },
        {
            'customFieldID': 317867,
            'name': 'IP Address',
            'value': samIp
            },
        {
            'customFieldID': 318304,
            'name': 'MAC Address',
            'value': samMac
            },
        {
            'customFieldID': 317861,
            'name': 'Manufacturer',
            'value': samMan
            },
        {
            'customFieldID': 316581,
            'name': 'Model Number',
            'value': samMod
            },
        {
            'customFieldID': 318307,
            'name': 'Operating System',
            'value': samOs
            },
        {
            'customFieldID': 327493,
            'name': 'Samanage Url',
            'value': samUrl
            },
        {
            'customFieldID': 316582,
            'name': 'Serial Number',
            'value': samSerial
            }
        ]
                          })
    # Use a HTML PUT action to update the FMX listing
    r = requests.put(destUrl,headers=headers,auth=(fmxUser,fmxPass),data=fmxJson)
    print(samName + " Update: " + str(r))


def fmxAdd(source):
    # If the listing doesn't appear we have to create a new listing. Unpack the source for the JSON data
    samIp = source.get('ip')
    samMan = source.get('manufacturer')
    samMod = source.get("model")
    samOs = source.get('os')
    samSerial = source.get('serial')
    samMac = source.get('mac')
    samTag = source.get('tag')
    samUrl = source.get('url')
    destUrl = fmx['fmxPostUrl']
    samName = source.get('name')
##    if samType == 'Workstation':
##        fmxType = 122218
##    elif samType == 'Server + VMware':
##        fmxType = 'server'
##    elif samType == 'Tablet':
##        fmxType = 'tablet
    fmxJson = json.dumps({
  "kind": "Equipment",
  "id": 771485,
  "tag": samName,
  "hierarchicalName": samName,
  "equipmentTypeID": 122218,
  "buildingID": 146283,
  "customFields": [
    {
      "customFieldID": 318419,
      "name": "Frederic County Asset Tag",
      "value": samTag
    },
    {
      "customFieldID": 317867,
      "name": "IP Address",
      "value": samIp
    },
    {
      "customFieldID": 318304,
      "name": "MAC Address",
      "value": samMac
    },
    {
      "customFieldID": 317861,
      "name": "Manufacturer",
      "value": samMan
    },
    {
      "customFieldID": 316581,
      "name": "Model Number",
      "value": samMod
    },
    {
      "customFieldID": 318418,
      "name": "NRADC Asset Tag"
    },
    {
      "customFieldID": 318307,
      "name": "Operating System",
      "value": samOs
    },
    {
      "customFieldID": 327493,
      "name": "Samanage Url",
      "value": samUrl
    },
    {
      "customFieldID": 316582,
      "name": "Serial Number",
      "value": samSerial
    },
    {
      "customFieldID": 316584,
      "name": "Warranty Date"
    }
      ],
    })
    # Use a HTML POST action to create a new entry
    r = requests.post(destUrl,auth=(fmxUser,fmxPass),headers=headers,data=fmxJson)
    print(samName + " Addition: " + str(r))

        
    

# Get the data from Samanage
req = requests.get(samanage_url,headers=samanage_headers).json()
r = requests.get(get_equip_url,auth=(fmxUser,fmxPass), headers=headers).json()


samList = []
# Get data out of Samanage and put it into a local List. Each Item is a dictionary inside of the List
for e in range(len(req)):
    sourceName = req[e].get('name')
    sourceId = req[e].get('id')
    sourceIp = req[e].get('ip')
    sourceBios = req[e].get('bioses')
    sourceMan = sourceBios[0].get('manufacturer')
    sourceMod = sourceBios[0].get('model')
    sourceOs = req[e].get('operating_system')
    sourceTag = req[e].get('tag')
    sourceCat = req[e].get('category')
    sourceType = sourceCat.get('name')
   # sourceType = req[e].get('type')
    sourceSerial = req[e].get('serial_number')
    sourceNet = req[e].get('networks')
    sourceMac = sourceNet[0].get('mac_address')
    sourceUrl = samUrlBase + str(sourceId) +'-'+ sourceName
    samDict = {'id': sourceId , 'name': sourceName, 'ip': sourceIp, 'manufacturer': sourceMan, 'type': sourceType, 'model': sourceMod, 'os': sourceOs, 'serial':sourceSerial, 'mac': sourceMac, 'tag': sourceTag, 'url': sourceUrl}
    samList.append(samDict)


#Get the data from FMX
r = requests.get(get_equip_url,auth=(fmxUser,fmxPass), headers=headers).json()
fList = []
# In FMX we will grab the ID number and the Tag. 
for i in range(len(r)):
    destName = r[i].get('tag')
    destId = r[i].get('id')
    fmDict = {'name': destName,'id': destId}
    fList.append(fmDict)



# Compare the tage from FMX with the name from the Samanage List
for i in range(len(samList)):
    name  = samList[i].get('name')
    sourceId = samList[i].get('id')
    for j in range(len(fList)):
        destName = fList[j].get('name')
        destId = fList[j].get('id')
        if name == destName:
            # If the names match, we will run fmxUpdate to update the listing in FMX
            fmxUpdate(samList[i],destId)
    if not next((item for item in fList if item['name'] == name), False):
        # If the item doesn't exist in the FMX Inventory we will add it as new
        fmxAdd(samList[i])
   

      


# If item exists, create a PUT action


# If the item doesn't exist, create a POST action

