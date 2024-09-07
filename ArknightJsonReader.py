import requests
import json

class ArknightsDataProcessor:
    def __init__(self):
        self.config = {}
        self.operator_dict = {}
        self.urls = {
            'EN': "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData_YoStar/main/en_US/gamedata/excel/character_table.json",
            'CN': "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/character_table.json"
        }

    def load_config(self):
        try:
            with open("dataConfig.txt", 'r') as file:
                for line in file:
                    key, value = line.strip().split(':')
                    self.config[key] = value
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
            self.config = default_config  

    def extract_json(self, data):
        for key, value in data.items():
            if value.get('subProfessionId') != "notchar2":
                self.operator_dict[key] = {k: value.get(v) for k, v in self.config.items()}
            else:
                print('Removed:', value.get('name'))
        self.dump_json()

    def dump_json(self):

        while True:
            file_name = input("Name your file: ")
            if file_name:
                with open(f"{file_name}.json", "w") as file:
                    json.dump(self.operator_dict, file, indent=4)
                break
            else:
                print("Input a proper file name.")

    def set_json(self, region):
        file_path = f'char/arknightChar{region}.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        self.extract_json(data)

    def download_json(self, url, region):
        file_path = f"char/arknightChar{region}.json"
        try:
            response = requests.get(url)
            response.raise_for_status()  
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print("File downloaded successfully.")
            self.set_json(region)
        except requests.exceptions.RequestException as e:
            print("Failed to download file. Error:", str(e))

   
    def menu(self):
        while True:
            choice = input("Choose an option:\n"
                           "[1] Download EN Json File\n"
                           "[2] Download CN Json File\n"
                           "[3] Edit URLs\n"
                           "[4] Exit\n"
                           "Enter your choice (1, 2, 3, or 4): ")
            if choice == "1":
                self.download_json(self.urls['EN'], 'EN')
            elif choice == "2":
                self.download_json(self.urls['CN'], 'CN')
            elif choice == "3":
                self.edit_urls()
            elif choice == "4":
                break
            else:
                print("Invalid selection. Please enter 1, 2, 3, or 4.")

    def edit_urls(self):

        print("Current URLs:")
        print(f"EN URL: {self.urls['EN']}")
        print(f"CN URL: {self.urls['CN']}")
        region = input("Which URL would you like to edit? (EN or CN): ").upper()
        if region in self.urls:
            new_url = input(f"Enter the new URL for {region}: ")
            self.urls[region] = new_url
            print(f"{region} URL updated successfully.")
        else:
            print("Invalid region. Please enter 'EN' or 'CN'.")


if __name__ == "__main__":
    ark = ArknightsDataProcessor()
    ark.load_config()
    ark.menu()
