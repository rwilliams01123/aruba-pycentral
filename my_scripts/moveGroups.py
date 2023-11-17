import requests
import json
import csv


def main():
    #API_KEY = 'EInis01razrxlEaalR0MFEYjkb8qphri'
    API_KEY = input("API Key: ")
    file_location = input("File location: ").strip()
    #
    apList = list()
    with open(file_location, newline='', encoding='utf-8-sig') as f:
        for i in csv.reader(f):
            apList.append(i[0])
    #


    apClusters = []
    start = 0
    end = len(apList)
    step = 50
    for i in range(start, end, step):
        x = i
        apClusters.append(apList[x:x+step])

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    for i in apClusters:
        url = "https://apigw-prod2.central.arubanetworks.com/configuration/v1/devices/move"
        payload = json.dumps(
            {
                "group": "Funston",
                "serials": i
            }
        )
        response = requests.request("POST", url, headers=headers, data=payload)
        print(f"{response} | {response.text}")


if __name__ == "__main__":
    main()
