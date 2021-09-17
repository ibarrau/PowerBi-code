'''
LADATAWEB 
Script writen by ibarrau

REQUEST RESTRICTIONS
This operation is only supported for datasets in a new workspace (V2 workspace)
The user issuing the request needs to have Build permissions for the dataset.
The Allow XMLA endpoints and Analyze in Excel with on-premises datasets tenant setting needs to be enabled.
Datasets hosted in AsAzure or live connected to an on premise Analysis Services model are not supported.
Only one query returning one table of maximum 100k rows is allowed. Specifying more than one query will return an error.

NOTE: DAX query failures will be returned with a failure HTTP status (400)
'''

import json
import pandas as pd
import requests

# Connection Settings
TENANT_ID = 'xxxxx-xxxx-xxxx-xxxx-xxxxxxxxx'
POWER_BI_RESOURCE_ENDPOINT = "https://analysis.windows.net/powerbi/api"
MICROSOFT_OAUTH2_API_ENDPOINT = "https://login.microsoftonline.com/" + TENANT_ID + "/oauth2/token/"

# Credentials
power_bi_username = 'user@company.com.ar'
power_bi_password = 'password'
power_bi_client_id = 'xxxxxx-xxxx-xxxx-xxxxx-xxxx-xxxx-xxxx-xxxxxxxxx' #also known as AppID
dataset = 'xxxxx-xxxx-xxxx-xxxx-xxxxxxxxx'

# Method to connect with the previous parameters and get the bearer token to use Power Bi API
def get_auth_token(power_bi_client_id, power_bi_username, power_bi_password):
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
    except Exception as e:
        print(e)

# Post Request method to run the query against the XMLA dataset endpoint returning a pandas dataframe parsed from json response 
def post_dax_query(query, auth_token, dataset):
    try: 
        url= "https://api.powerbi.com/v1.0/myorg/datasets/"+dataset+"/executeQueries"        
        body = {"queries": [{"query": query}], "serializerSettings": {"incudeNulls": "true"}}
        headers={'Content-Type': 'application/json', "Authorization": "Bearer {}".format(auth_token)}
        res = requests.post(url, data = json.dumps(body), headers = headers)
        #get columns from json response - keys from dict
        columnas = list(res.json()['results'][0]['tables'][0]['rows'][0].keys())
        #get the number of rows to loop data
        filas = len(res.json()['results'][0]['tables'][0]['rows'])        
        #get data from json response - values from dict
        datos = [list(res.json()['results'][0]['tables'][0]['rows'][n].values()) for n in range(filas-1)]
        #build a dataframe from the collected data
        df = pd.DataFrame(data=datos, columns=columnas)
        print(df.head())
        return res
    except requests.exceptions.HTTPError as ex:
        print(ex)
    except Exception as e:
        print(e)
        
# Executions to make it happen
auth_token = get_auth_token(power_bi_client_id, power_bi_username, power_bi_password)

# Write your DAX  query inside the query parameter. There you have an example.
query = "EVALUATE VALUES(TablaFecha[Mes])"

# Capture dataframe in df 
df = post_dax_query(query, auth_token, dataset)

# Have fun with your df




