import sys
import json
from datetime import date, timedelta
import pandas as pd
import requests
import time

POWER_BI_RESOURCE_ENDPOINT = "https://analysis.windows.net/powerbi/api"
MICROSOFT_OAUTH2_API_ENDPOINT = "https://login.windows.net/common/oauth2/token/"

power_bi_username = 'usuario'
power_bi_password = 'pass'
power_bi_client_id = 'XXXX-XXXX-XXXX-XXXX'

def get_auth_token_requests(power_bi_client_id, power_bi_username, power_bi_password):
    try:
        url = MICROSOFT_OAUTH2_API_ENDPOINT
        body = {
            "resource":POWER_BI_RESOURCE_ENDPOINT, 
            "client_id":power_bi_client_id,
            "grant_type":"password",
            "username":power_bi_username,
            "password":power_bi_password,
            "scope":"openid"                    
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
            }
        r = requests.post(url = url, data = body, headers = headers)
        access_token = r.json().get('access_token')
        return access_token
    except requests.exceptions.HTTPError as ex:
        print(ex)
    
def get_activities_requests(auth_token):
    columnas = ['Id', 'RecordType', 'CreationTime', 'Operation', 'OrganizationId',
       'UserType', 'UserKey', 'Workload', 'UserId', 'ClientIP', 'UserAgent',
       'Activity', 'ItemName', 'WorkSpaceName', 'DatasetName', 'WorkspaceId',
       'ObjectId', 'DatasetId', 'DataConnectivityMode', 'IsSuccess',
       'RequestId', 'ActivityId', 'TableName', 'LastRefreshTime']
    df_total = pd.DataFrame(columns=columnas)
    ayer = date.today()- timedelta(days=1)
    start = ayer.strftime("'%Y-%m-%dT%H:%M:00.000Z'")
    end = ayer.strftime("'%Y-%m-%dT23:59:59.000Z'")
    url = "https://api.powerbi.com/v1.0/myorg/admin/activityevents?startDateTime={}&endDateTime={}".format(start, end)
    ban = True   
    contar = 0    
    try:
        while(ban):        
            response = requests.get(url,
                headers={'Content-Type': 'application/json', "Authorization": "Bearer {}".format(auth_token)}
                )            
            js = json.dumps(response.json()["activityEventEntities"])
            df = pd.read_json(js)
            print(response.status_code)
            contar = contar +1
            print(contar)
            print(df.head())
            print(response.json()["continuationUri"])
            df_total = df_total.append(df, sort=True, ignore_index=True)
            print(df_total.head())
            if response.json()["continuationUri"] == None:
                ban=False
            url = response.json()["continuationUri"]   
        return df_total
    except requests.exceptions.Timeout:
        print("ERROR: The request method has exceeded the Timeout")
    except requests.exceptions.TooManyRedirects:
        print("ERROR: Bad URL try a different one")
    except requests.exceptions.RequestException as e:
        print("Catastrophic error.")
        raise SystemExit(e)
    except requests.error as e:
        status_code = e.code
        print(status_code)
        print(e) 
    except Exception as ex:
        print(ex)

auth_token = get_auth_token_requests(power_bi_client_id, power_bi_username, power_bi_password)

frame = get_activities_requests(auth_token)
