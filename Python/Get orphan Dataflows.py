
'''
  /¯¯¯¯¯¯¯¯¯\
 /           \
|   |   __    |  *********************************************
|   |  |  \   |  Code writen by ibarrau
|   |  |  |   |
|   |__|_ |   |  La Data Web 
|      |__/   |  *********************************************
 \            /
  \__________/
  
REQUEST RESTRICTIONS
This operation is only supported by admin permission
The request used to track the dataflows in datasets has a limitations of 200 requests. 
Each one of those is using a workspace param, so it will ONLY work if you have less than 200 workspaces in your tenant.
'''

import json
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

def get_orphan_dataflows_preview(auth_token):
	"""Returns a list of all dataflows that are not used by a dataset.
	"""
	try:
        # Get all the Collaborative workspaces IDs that contain at least one dataflow and store them in a list. 
		url_wp = "https://api.powerbi.com/v1.0/myorg/admin/groups?$expand=dataflows&$top=5000"
		res_wp= requests.get(url_wp, headers={'Content-Type': 'application/json', "Authorization": "Bearer {}".format(auth_token)})
        res_wp.raise_for_status()
		workspaces = [res_wp.json()["value"][i]["id"] for i in range(len(res_wp.json()["value"])) if res_wp.json()["value"][i]["dataflows"] != []]
        
        # Check if the lista contains more than 200 items. The API has a 200 workspaces limitations to check the values.
        if len(workspaces) > 200:            
            return "You can't use this request because you have more than 200 workspaces (limitation)."
		
        # Get all dataflows in the tenant and store them in a list
		url_df = "https://api.powerbi.com/v1.0/myorg/admin/dataflows"
		res_df = requests.get(url_df, headers={'Content-Type': 'application/json', "Authorization": "Bearer {}".format(auth_token)})
        res_df.raise_for_status()
		dataflows = [res_df.json()["value"][i]["objectId"] for i in range(len(res_df.json()["value"]))]
		
        # Create empty list of active and orphan dataflows
		actives = []
		orphans = []
		
        # Loop one by one all the workspaces checking which datasets in there have dataflows as source to create the active dataflows list
		for wp in workspaces:
			url = "https://api.powerbi.com/v1.0/myorg/admin/groups/{}/datasets/upstreamDataflows".format(wp)
			res = requests.get(url, headers={'Content-Type': 'application/json', "Authorization": "Bearer {}".format(auth_token)})
			if res.text != '' or res.status_code != 200:
				actives.extend( [res.json()["value"][i]["dataflowObjectId"] for i in range(len(res.json()["value"])) ] )        
        
        # Loop all the dataflows checking if they are in the active list. If they are not they are added to orphans 
		for df in dataflows:
			if df not in actives:
				orphans.append(df)
		
		return orphans
	except requests.exceptions.HTTPError as ex:
		print("HTTP Error: ", ex, "\nText: ", ex.response.text)
	except requests.exceptions.RequestException as e:
		print("Request exception: ", e)
	except Exception as ee:
		print("Exception: ", ee)        
        
        
# Executions to make it happen
auth_token = get_auth_token(power_bi_client_id, power_bi_username, power_bi_password)

# Return orphans dataflows
get_orphan_dataflows_preview(auth_token)