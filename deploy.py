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
from simplepbi import token
from simplepbi import imports

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
                try:
                    #it = self.list_items(semantic_model_workspace_id)
                    semantic_model_id = "asdasd"#[i['id'] for i in it['value'] if i['displayName']==semantic_model_name and i['type']=="SemanticModel" ]
                    if semantic_model_id == []:
                        raise Exception("Semantic Model {} does not exist in the specified workspace.".format(semantic_model_name))
                except Exception as e:
                    print("Error: ", e)
                    
                del pbir_json['datasetReference']['byPath']
                
                # Add a new JSON object to the "byConnection" property
                pbir_json['datasetReference']['byConnection'] = {
                    "connectionString": None,
                    "pbiServiceModelId": None,
                    "pbiModelVirtualServerName": "sobe_wowvirtualserver",
                    "pbiModelDatabaseName": semantic_model_id[0],
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
            #encoded_contents = base64.b64encode(file_contents).decode("utf-8")

            # Add the file to the Parts array
            parts.append({
                "Path": file_path,
                #"Payload": encoded_contents,
                "PayloadType": "InlineBase64"
            })
    print(parts)
          
            
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
            #encoded_contents = base64.b64encode(file_contents).decode("utf-8")

            # Add the file to the Parts array
            parts.append({
                "Path": file_path,
                #"Payload": encoded_contents,
                "PayloadType": "InlineBase64"
            })
    print(parts)

# Set variables
Throw_exception = ""
#Workspace_name = Folder_Name.split("/")[-1]
Workspace = sys.argv[1]

list_files = " ".join(sys.argv[5:])
Folder_Name = "/".join(list_files.split("/")[:-1])
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

# import report from path
try:    
    if list_files.split(".")[-1] == "Report":            
        print("running report")
        partes_report(list_files)
    else:
        print("running semantic")
        partes_semantic(list_files)
except Exception as e:
    print("Error_: ", e)
    raise Exception(e)

    
