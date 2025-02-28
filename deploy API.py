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
@........|____| |  | |...*   *.@    Copyright © 2025 Ignacio Barrau
@   .       . | |__| |. *     *@
@   .       . |_____/ . *     *@    *********************************************
@   .       .         . *     *@
@   .       .         . *******@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

This script is used to deploy Power BI reports or semantic models to a workspace. It is called from the GitHub Action. It uses the simplepbi library and LaDataWeb API to deploy.
 
'''

import sys 
import os
import sys 
import json
import base64
import requests
from simplepbi import token
from simplepbi.fabric import core
# from simplepbi import ladataweb

            
# Set variables
Throw_exception = ""
Workspace = sys.argv[1]

# Get list of file path folders with changes
list_files = " ".join(sys.argv[5:])

# Get Workspace Name from folder considering the second item of the path as the workspace [1]. /Folders/Workspace/**
Workspace_Name = list_files.split(",")[0].split("/")[:-1][1]
print("The arguments are: " , str(sys.argv))

# Show extraction
print("Folder_Name: " + Workspace_Name, "\nWorkspace: " + Workspace, "\nFolders: " + str(list_files))

# Get list of files to import
#list_files = [item for item in Files.split(",") if item[-4:]=="pbix" and item.split("/")[0] ==Folder_Name]
#print("list_files: " + str(list_files))

# Log into Power BI
TENANT_ID = sys.argv[2]
power_bi_client_id = sys.argv[3]
power_bi_secret = sys.argv[4]
print("Environment Variables loaded.")

# Get token for Fabric API
t = token.Token(TENANT_ID, power_bi_client_id, None, None, power_bi_secret, use_service_principal=True)

# Create item objects to deploy and workspace to find the id by name
it = core.Items(t.token)
wp = core.Workspaces(t.token)

# Find workspace id by name
try:
    areas = wp.list_workspaces(roles="admin, member, contributor, viewer")
    workspace_id = [i['id'] for i in areas['value'] if i['displayName']==Workspace_Name and i['type']=="Workspace" ]
    if workspace_id == []:
        raise Exception("Workspace {} does not exist.".format(Workspace_Name))
except Exception as e:
    print("Error: ", e)
    sys.exit(1)

print("Token generated.\nWorkspace id found: " + str(workspace_id))

# Remove text after .SemanticModel or .Report to optimize deployment when modify multiple files of single item
sm_items_deploy = []
re_items_deploy = []
# Creating two lists to organize semantic models first at deploys and then reports
for files in list_files.split(","):
    try:
        if ".Report" in files: # Another alternative check specific folder .split(".")[-1] == "Report"            
            item_path = files.split(".Report")[0]+".Report"
            re_items_deploy.append(item_path)
        else:            
            if ".SemanticModel" in files:
                item_path = files.split(".SemanticModel")[0]+".SemanticModel"
            else:
                item_path = files.split(".Dataset")[0]+".Dataset"
            sm_items_deploy.append(item_path)        
    except Exception as e:
        print("Error_: ", e)
        raise Exception(e)
items_deploy = sm_items_deploy + re_items_deploy


# Deploy Report or semantic model change by checking files modification at Report or SemanticModel folder.
for pbi_item in list(set(items_deploy)):
    try:
        item_name = pbi_item.split("/")[-1].split(".")[0]
        if item_name == "":
            raise Exception("Make sure the path doesn't en in / or \\ at the end.")
        else:
            print("Item name: ", item_name)
        if ".Report" in pbi_item: # Another alternative check specific folder .split(".")[-1] == "Report"
            print("Running report deployment to path: " + pbi_item)
            # Build report parts for deploy checking semantic model workspace
            parts = it.build_report_parts(workspace_id[0], pbi_item)
            body = {
                "ldw-api-key": "test_key",
                "btoken": t.token,
                "workspace_id": workspace_id[0],
                "item_name": item_name,
                "item_type": "Report",
                "parts": parts
            }
            res = requests.post(url="https://ldw-api.azurewebsites.net/api/deploy-powerbi-item", headers={'Content-Type': 'application/json'}, data=json.dumps(body))            
            # ladataweb.deploy_report(ldw_api_key, t.token, workspace_id[0], item_name, "Report", parts)
        else:
            print("Running semantic model deployment to path: " + pbi_item)
            # Build semantic model parts for deploy
            parts = it.build_semantic_model_parts(workspace_id[0], pbi_item)
            body = {
                "ldw-api-key": "test_key",
                "btoken": t.token,
                "workspace_id": workspace_id[0],
                "item_name": item_name,
                "item_type": "SemanticModel",
                "parts": parts
            }
            res = requests.post(url="https://ldw-api.azurewebsites.net/api/deploy-powerbi-item", headers={'Content-Type': 'application/json'}, data=json.dumps(body))
            # ladataweb.deploy_semantic_model(ldw_api_key, t.token, workspace_id[0], item_name, "SemanticModel", parts)
        print(res.text)
    except Exception as e:
        print("Error_: ", e)
        raise Exception(e)


