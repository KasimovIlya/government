import requests
import json
from firebase import firebase

# class for saving info
class Contract:
    number = ''
    stage = ''
    contract_url = ''
    sign_date = ''
    price = ''
    customer_name = ''
    task_name = ''

    def __init__(self, number, stage, contract_url, sign_date, price, customer_name, task_name):
        self.number = number
        self.stage = stage
        self.contract_url = contract_url
        self.sign_date = sign_date
        self.price = price
        self.customer_name = customer_name
        self.task_name = task_name

#input
print("Введите сумму, начиная с которой мы будкем искать:")
start = int(input())
print("Введите сумму,до которой мы будкем искать:")
finish = int(input())
url = "http://openapi.clearspending.ru/restapi/v3/contracts/search/?pricerange={}-{}".format(start, finish)
firebase_url = "https://government-aa9aa.firebaseio.com"

#making request to API
information = requests.get(url).text
dic = json.loads(information)

#making empty list for saving info about contracts
allContracts = []

#parse
if "contracts" in dic:
    contracts = dic["contracts"]

    if "data" in contracts:
        contracts_list = contracts["data"]
        print(contracts_list)

        for contract in contracts_list:
            number = contract["regNum"]
            stage = contract["currentContractStage"]
            contract_url = contract["contractUrl"]
            sign_date = contract["signDate"]
            price = contract["price"]
            task_name = ''
            smth = contract["customer"]
            customer_name = smth["fullName"]
            smth2 = contract["products"]
            task_name2 = smth2[0]
            task_name = task_name2["name"]




            allContracts.append(Contract(number, stage, contract_url, sign_date, price, customer_name, task_name))

#putting info we collected to DB
db = firebase.FirebaseApplication(firebase_url, None)
for contract in allContracts:
    print(contract.__dict__)
    db.post("/contracts", contract.__dict__)
