import requests
import json
import csv


def main():
    API_KEY = input("API Key: ")
    csv_location = input("CSV Location:\n")

    with open(csv_location, 'r', encoding='utf-8-sig') as f:
        apcsv = list(csv.DictReader(f))

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    for i in apcsv:
        url = (f"https://apigw-prod2.central.arubanetworks.com/"
               f"configuration/v1/ap_settings/{i['serial']}")
        payload = json.dumps({"hostname": i['name'], "ip_address": "0.0.0.0"})
        response = requests.request("POST", url, headers=headers, data=payload)
        print(f"{response} | {response.text}")


if __name__ == "__main__":
    main()
