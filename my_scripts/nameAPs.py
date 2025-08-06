import requests
import json
import csv
import tools_rwilliams01123 as tools


def main():
    API_KEY = input("Access Token: ")
    ap_list = tools.quick_import_csv()

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    for i in ap_list:
        serial = i['serial']
        new_name = i['new_hostname']
        #
        url = f"https://apigw-prod2.central.arubanetworks.com/configuration/v2/ap_settings/{serial}"
        get_response = tools.api_call_verify('get', url, headers, None)
        # Modify hostname
        get_response['hostname'] = new_name
        # format get_response for requests call
        payload = json.dumps(get_response)
        post_response = tools.api_call_verify('post', url, headers, payload)
        print("\n")


if __name__ == "__main__":
    main()
