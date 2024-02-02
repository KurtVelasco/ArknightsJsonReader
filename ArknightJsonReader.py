import requests
import json

# Use utf-8 since some of the char in json are in CN
raw = None
data = None
operatorDict = {}
config = {}
downloadURL = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData_YoStar/main/en_US/gamedata/excel/character_table.json"


#In the textfile, just add your own data that you want to take
#refer to the Json File
def LoadConfig():
    global config 
    try:
        with open("dataConfig.txt", 'r') as file:
            for line in file:
                key, value = line.strip().split(':')
                config[key] = value
    except FileNotFoundError:
        default_config = {
            'name': 'name',
            'nationID': 'nationId',
            'class': 'profession',
            'subclass': 'subProfessionId',
            'recruitment': 'itemObtainApproach',
            'rarity': 'rarity'
        }
        with open("dataConfig.txt", 'w') as file:
            for key, value in default_config.items():
                file.write(f"{key}:{value}\n")
        config = default_config  
        
def ExtractJson():
    for key, value in data.items():
        if(value.get('subProfessionId') != "notchar2" and (value.get('subProfessionId') != "notchar2")):
            operatorDict[key] = {k: value.get(v) for k, v in config.items()}
        else:
            print('removed ' + value.get('name'))
    DumpJson()
    
            
def DumpJson():
    while True:
        uInput = input("Name your file: ")
        if(len(uInput) > 0):
           with open(uInput + ".json", "w") as file:
                json.dump(operatorDict, file, indent=4) 
                break
        else:
            print("Input a proper file name ")
        
           
def SetJson(region):
    global raw, data
    raw = open('char/arknightChar'+region+'.json', 'r', encoding='utf-8')
    data = json.load(raw)
    ExtractJson()
            
   
def DownloadJson(url,region):
    defaultFilePath = "char/arknightChar"+region+".json"
    response = requests.get(url)
    if response.status_code == 200:
        with open(defaultFilePath, 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully")
        SetJson(region)
    else:
        print("Failed to download file:", response.status_code)
        
def Menu():
    regionType = 'EN'
    while True:
        uInput = input("Downloaded from @Kengxxiao at github choose which version: \n"
                       "[1] EN Json File\n"
                       "[2] CN Json File\n"
                       "Enter your choice (1 or 2): ")
        if uInput == "1":
            downloadURL = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData_YoStar/main/en_US/gamedata/excel/character_table.json"
            DownloadJson(downloadURL,'EN')
            break
        elif uInput == "2":
            DownloadJson(downloadURL,'CN')
            downloadURL = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/character_table.json"
            break
        else:
            print("Invalid selection. Please enter 1 or 2.")


LoadConfig()
Menu()
        

       