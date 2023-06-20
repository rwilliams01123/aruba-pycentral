#!/usr/bin/env python3
import json
import csv
import os
import re
from pprint import pprint
import requests


def main():
    API_KEY = input("API Key: ")
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    url = "https://apigw-prod2.central.arubanetworks.com/monitoring/v2/aps?group=CHS"
    payload = {}
    headers = {'Authorization': f'Bearer {API_KEY}'}
    #
    response = requests.request("GET", url, headers=headers, data=payload)
    #
    aplist = json.loads(response.text)
    aps = [
        {'serial': i['serial'], 'name': i['name']}
        for i in aplist['aps']
    ]

    keys = [x for i in aps for x in i]
    csvheader = [ele for count, ele in enumerate(keys) if ele not in keys[:count]]
    with open('aps.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csvheader)
        for i in aps:
            csvrow = [i.get(x) for x in csvheader]
            writer.writerow(csvrow)
    #
    print("\nComplete! Saved AP list at: "+os.getcwd()+"/aps.csv\n\n\n")

if __name__ == "__main__":
    main()
