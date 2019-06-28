import sys
import json
import urllib.request as urllib2
import urllib
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
        payload = "resource={}&client_id={}&grant_type=password&username={}&password={}&scope=openid".format(urllib.parse.quote_plus(POWER_BI_RESOURCE_ENDPOINT), urllib.parse.quote_plus(power_bi_client_id), urllib.parse.quote_plus(power_bi_username), urllib.parse.quote_plus(power_bi_password)).encode("utf-8")
        #with urllib2.urlopen(req,payload) as response:
        #    resp = response.read()
        #    print(resp)
        response = urllib2.urlopen(req, payload)
        response_read = response.read().decode('utf8').replace("'", '"')
        json_response = json.loads(response_read )
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
        }).encode("utf-8")

        response = urllib2.urlopen(req, payload)
        
        return True
    except urllib2.HTTPError as e:
        status_code = e.code
        print(status_code)
        print(e)

        return False

auth_token = get_auth_token(power_bi_client_id, power_bi_username, power_bi_password)
refresh_dataset(auth_token, power_bi_group, power_bi_dataset)

#if it usually works and then a 404 error is returned you may raise to power bi 8 refreshes limit
