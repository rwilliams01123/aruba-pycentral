import requests
import json
import csv
import tools


def main():
    API_KEY = input("API Key: ")
    ap_list = tools.quick_import_csv()

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    for i in ap_list:
        # Get per AP settings
        url = (f"https://apigw-prod2.central.arubanetworks.com/"
               f"/configuration/v1/ap_settings_cli/{i['serial']}")
        get_response = tools.api_call_verify('get', url, headers, None)
        # Modify hostname
        get_response[1] = f"  hostname {i['name']}"
        !
        # format get_response for requests call
        payload = json.dumps({"clis": get_response})
        post_response = tools.api_call_verify('post', url, headers, payload)
        #
        #
        '''
        url = (f"https://apigw-prod2.central.arubanetworks.com/"
               f"configuration/v1/ap_settings/{i['serial']}")
        payload = json.dumps({"hostname": i['name'], "ip_address": "0.0.0.0"})
        response = tools.api_call_verify('POST', url, headers, payload)
        '''


if __name__ == "__main__":
    main()
