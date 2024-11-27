'''.
           @@@@@@@@@@
       @@@@..........@@@@
    @@@         .        @@@
  @@.           .         . @@
 @  .     _     .         .   @
@........| |...................@    *********************************************
@      . | |   _____  .        @
@      . | |  |  __ \ .        @    La Data Web Script
@      . | |__| |  | |.   ***  @
@........|____| |  | |...*   *.@    Copyright © 2023 Ignacio Barrau
@   .       . | |__| |. *     *@
@   .       . |_____/ . *     *@    *********************************************
@   .       .         . *     *@
@   .       .         . *******@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

This script is used to deploy Power BI reports to a workspace. It is called from the Azure DevOps pipeline. It uses the simplepbi library to import the reports.
 
'''

import os
import sys 
import json
import base64
import requests
from simplepbi import token
from simplepbi import imports

def update(auth_token, workspace_id, item_id, body):
    '''This function will import a PBIX file from GitHub to Power BI
     ### Parameters
    ----
    owner: str
        The account owner of the repository. The name is not case sensitive. For example: https://dev.azure.com/ibarrau/ the organization name is ibarrau    
    workspace_id: str uuid
        The Power Bi workspace id. You can take it from PBI Service URL    
    ### Returns
    ----
    Dict:
        Response 200 Ok
    '''
    try:           
        
        url="https://api.fabric.microsoft.com/v1/workspaces/{}/items/{}/updateDefinition".format(workspace_id, item_id)
        #headers = {'Content-Type': 'multipart/form-data', "Authorization": "Bearer {}".format(auth_token)}
        headers = {'Content-Type': 'application/json; charset=utf-8', "Authorization": "Bearer {}".format(auth_token)}
        
        
        res = requests.post(url, data = body, headers=headers)
        res.raise_for_status()
        if res.status_code==202:
            print("Request accepted, item provisioning in progress. Please wait.")
        print("Operation id: ", res.headers['x-ms-operation-id'])
        return res
    except requests.exceptions.HTTPError as ex:
        print("HTTP Error: ", ex, "\nText: ", ex.response.text)
    except requests.exceptions.RequestException as e:
        print("Request exception: ", e)

def partes_report(item_path):
    parts = []

    item_name = item_path.split("/")[-1].split(".")[0]
    if item_name == "":
        raise Exception("Make sure the path doesn't en in / or \\ at the end.")
    else:
        print("Item name: ", item_name)

    # Iterate through the files in the item_path
    for root, dirs, files in os.walk(item_path):
        # Skip folders with the name ".pbi"
        if os.path.basename(root) == ".pbi":
            continue
        print("Checking folder: ", item_path, " in root: ", root, " and files: ", files)
        for file in files:
            # Skip files with the name "item.*.json"
            if file.startswith("item.") and file.endswith(".json"):
                continue
            if file == "cache.abf":
                continue
            if file.endswith(".pbir"):
                # Load the JSON file
                with open(item_path +'/definition.pbir', 'r') as f:
                    pbir_json = json.load(f)
                    
                # Remove the "byPath" item
                semantic_model_name = pbir_json['datasetReference']['byPath']['path'].split("/")[-1].split(".")[0]                    
                #print("Looking for id of semantic model {} in workspace id {} related to the report".format(semantic_model_name, semantic_model_workspace_id))               
                    
                del pbir_json['datasetReference']['byPath']
                
                # Add a new JSON object to the "byConnection" property
                pbir_json['datasetReference']['byConnection'] = {
                    "connectionString": None,
                    "pbiServiceModelId": None,
                    "pbiModelVirtualServerName": "sobe_wowvirtualserver",
                    "pbiModelDatabaseName": "4ba9ad01-163d-4a40-84a7-c5d32c7ef7e1",
                    "name": "EntityDataSource",
                    "connectionType": "pbiServiceXmlaStyleLive"
                }
                # Convert the PBIR JSON object to a string
                pbir_json_str = json.dumps(pbir_json)
                
                # Convert the string to UTF-8 bytes
                file_contents = pbir_json_str.encode('utf-8')
            else:            
                # Read the file contents
                with open(os.path.join(root, file), "rb") as f:
                    file_contents = f.read()
            
            # Get the file path relative to the project folder
            file_path = os.path.relpath(os.path.join(root, file), item_path).replace("\\","/")
        
            # Base64-encode the file contents
            encoded_contents = base64.b64encode(file_contents).decode("utf-8")

            # Add the file to the Parts array
            parts.append({
                "Path": file_path,
                "Payload": encoded_contents,
                "PayloadType": "InlineBase64"
            })
    body_update = {
        "definition": {
            "Parts": parts
        }
    }
    item_update_json = json.dumps(body_update, indent=4)
    update(t.token, Workspace, "48574d80-fc71-4733-b014-76ec11f5fa4c", item_update_json)
          
            
def partes_semantic(item_path):
    parts = []

    item_name = item_path.split("/")[-1].split(".")[0]
    if item_name == "":
        raise Exception("Make sure the path doesn't en in / or \\ at the end.")
    else:
        print("Item name: ", item_name)

    # Iterate through the files in the item_path
    for root, dirs, files in os.walk(item_path):
        if os.path.basename(root) == ".pbi":
            continue
        for file in files:
            # Skip files with the name "item.*.json"
            if file.startswith("item.") and file.endswith(".json"):
                continue
            if file == "cache.abf":
                continue

            # Get the file path relative to the project folder
            file_path = os.path.relpath(os.path.join(root, file), item_path).replace("\\","/")

            # Read the file contents
            with open(os.path.join(root, file), "rb") as f:
                file_contents = f.read()

            # Base64-encode the file contents
            encoded_contents = base64.b64encode(file_contents).decode("utf-8")

            # Add the file to the Parts array
            parts.append({
                "Path": file_path,
                "Payload": encoded_contents,
                "PayloadType": "InlineBase64"
            })
    body_update = {
    "definition": {
            "Parts": parts
        }
    }
    item_update_json = json.dumps(body_update, indent=4)
    update(t.token, Workspace, "4ba9ad01-163d-4a40-84a7-c5d32c7ef7e1", item_update_json)

# Set variables
Throw_exception = ""
Workspace = sys.argv[1]

list_files = " ".join(sys.argv[5:])

#Workspace Name just in case
Folder_Name = list_files.split(",")[0].split("/")[:-1][-1]
print("The arguments are: " , str(sys.argv))

print("Folder_Name: " + Folder_Name, "\nWorkspace: " + Workspace, "\nFolders: " + str(list_files))

# Get list of files to import
#list_files = [item for item in Files.split(",") if item[-4:]=="pbix" and item.split("/")[0] ==Folder_Name]
#print("list_files: " + str(list_files))

# log into Power BI
TENANT_ID = sys.argv[2]
power_bi_client_id = sys.argv[3]
power_bi_secret = sys.argv[4]
print("Environment Variables loaded.")

# get token and create objects
t = token.Token(TENANT_ID, power_bi_client_id, None, None, power_bi_secret, use_service_principal=True)
#it = core.Items(t.token)

print("Token generated")

for files in list_files.split(","):
    try:    
        if files.split(".")[-1] == "Report":            
            print("running report")
            partes_report(files)
        else:
            print("running semantic")
            partes_semantic(files)
    except Exception as e:
        print("Error_: ", e)
        raise Exception(e)

    
