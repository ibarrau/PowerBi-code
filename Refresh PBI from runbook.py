import sys
import json
import urllib
import urllib2
import time

POWER_BI_RESOURCE_ENDPOINT = "https://analysis.windows.net/powerbi/api"
MICROSOFT_OAUTH2_API_ENDPOINT = "https://login.windows.net/common/oauth2/token/"

power_bi_group = 'XXXX-XXXX-XXXX-XXXX'
power_bi_dataset = 'XXXX-XXXX-XXXX-XXXX'
power_bi_username = 'XXXX-XXXX-XXXX-XXXX'
power_bi_password = 'XXXX-XXXX-XXXX-XXXX'
power_bi_client_id = 'XXXX-XXXX-XXXX-XXXX'

def get_auth_token(power_bi_client_id, power_bi_username, power_bi_password):
    try:
        req = urllib2.Request(MICROSOFT_OAUTH2_API_ENDPOINT)
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        payload = "resource={}&client_id={}&grant_type=password&username={}&password={}&scope=openid".format(urllib.quote_plus(POWER_BI_RESOURCE_ENDPOINT), urllib.quote_plus(power_bi_client_id), urllib.quote_plus(power_bi_username), urllib.quote_plus(power_bi_password))
        response = urllib2.urlopen(req, payload)
        json_response = json.loads(response.read())
        access_token = json_response["access_token"]

        return access_token
    except urllib2.HTTPError as e:
        status_code = e.code
        print(status_code)

        return False

def refresh_dataset(auth_token, power_bi_group, power_bi_dataset):
    try:
        req = urllib2.Request("https://api.powerbi.com/v1.0/myorg/groups/{}/datasets/{}/refreshes".format(power_bi_group, power_bi_dataset))
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", "Bearer {}".format(auth_token))
        
        payload = json.dumps({
            "NotifyOption": "MailOnCompletion"
        })

        response = urllib2.urlopen(req, payload)
        
        return True
    except urllib2.HTTPError as e:
        status_code = e.code
        print(status_code)

        return False

auth_token = get_auth_token(power_bi_client_id, power_bi_username, power_bi_password)
refresh_dataset(auth_token, power_bi_group, power_bi_dataset)


''' Varios datasets.

import sys
import json
import urllib
import urllib2
import time

POWER_BI_RESOURCE_ENDPOINT = "https://analysis.windows.net/powerbi/api"
MICROSOFT_OAUTH2_API_ENDPOINT = "https://login.windows.net/common/oauth2/token/"

WAIT_AFTER_REFRESH_START_SECONDS = 15 
POLLING_INTERVAL_SECONDS = 30

def get_auth_token(power_bi_client_id, power_bi_username, power_bi_password):
    try:
        req = urllib2.Request(MICROSOFT_OAUTH2_API_ENDPOINT)
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        payload = "resource={}&client_id={}&grant_type=password&username={}&password={}&scope=openid".format(urllib.quote_plus(POWER_BI_RESOURCE_ENDPOINT), urllib.quote_plus(power_bi_client_id), urllib.quote_plus(power_bi_username), urllib.quote_plus(power_bi_password))
        response = urllib2.urlopen(req, payload)
        json_response = json.loads(response.read())
        access_token = json_response["access_token"]

        return access_token
    except urllib2.HTTPError as e:
        status_code = e.code
        print(status_code)

        return False

def refresh_dataset(auth_token, power_bi_group, power_bi_dataset):
    try:
        req = urllib2.Request("https://api.powerbi.com/v1.0/myorg/groups/{}/datasets/{}/refreshes".format(power_bi_group, power_bi_dataset))
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", "Bearer {}".format(auth_token))
        
        payload = json.dumps({
            "NotifyOption": "MailOnCompletion"
        })

        response = urllib2.urlopen(req, payload)
        
        return True
    except urllib2.HTTPError as e:
        status_code = e.code
        print(status_code)

        return False

def has_refresh_completed(auth_token, power_bi_group, power_bi_dataset):
    try:
        req = urllib2.Request("https://api.powerbi.com/v1.0/myorg/groups/{}/datasets/{}/refreshes?top=1".format(power_bi_group, power_bi_dataset))
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", "Bearer {}".format(auth_token))

        response = urllib2.urlopen(req)
        json_response = json.loads(response.read())
        refresh_status = json_response["value"][0]["status"]

        # Terminal statuses are 'Completed' and 'Failed'.
        # In progress status is 'Unknown'.
        if refresh_status in ('Completed', 'Failed'):
            return True
        else:
            return False

    except urllib2.HTTPError as e:
        status_code = e.code
        print(status_code)

        return True


payload = json.dumps({
    "power_bi_client_id": "XXXX-XXXX-XXXX-XXXX",
    "power_bi_username": "XXXX-XXXX-XXXX-XXXX",
    "power_bi_password": "XXXX-XXXX-XXXX-XXXX",

    "groups": {
        "XXXX-XXXX-XXXX-XXXX": {
            "datasets": [
                "XXXX-XXXX-XXXX-XXXX",
                "XXXX-XXXX-XXXX-XXXX"
            ]
        },
        "YYYY-YYYY-YYYY-YYYY": {
            "datasets": [
                "YYYY-YYYY-YYYY-YYYY",
                "YYYY-YYYY-YYYY-YYYY"
            ]
        },
    }
})

json_payload = json.loads(payload)

power_bi_client_id = json_payload["power_bi_client_id"]
power_bi_username = json_payload["power_bi_username"]
power_bi_password =  json_payload["power_bi_password"]

auth_token = get_auth_token(power_bi_client_id, power_bi_username, power_bi_password)

for power_bi_group in json_payload["groups"]:
    for power_bi_dataset in json_payload["groups"][power_bi_group]["datasets"]:
        refresh_dataset(auth_token, power_bi_group, power_bi_dataset)  
        time.sleep(WAIT_AFTER_REFRESH_START_SECONDS)

        while not has_refresh_completed(auth_token, power_bi_group, power_bi_dataset):
            time.sleep(POLLING_INTERVAL_SECONDS)

        print('Refresh complete.')
print('All refreshes completed.')

'''