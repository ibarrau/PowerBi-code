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
@........|____| |  | |...*   *.@    Copyright © 2024 Ignacio Barrau
@   .       . | |__| |. *     *@
@   .       . |_____/ . *     *@    *********************************************
@   .       .         . *     *@
@   .       .         . *******@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

This script is used to deploy Power BI reports to a workspace. It is called from the Azure DevOps pipeline. It uses the simplepbi library to import the reports.
 
'''

import sys 
from simplepbi import token
from simplepbi.fabric import core

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

# Deploy Report or semantic model change by checking files modification at Report or SemanticModel folder.
for files in list_files.split(","):
    try:
        if ".Report" in files: # Another alternative check specific folder .split(".")[-1] == "Report"            
            item_path = files.split(".Report")[0]+".Report"
            print("Running report deployment to path: " + item_path)
            it.simple_deploy_report(workspace_id[0], workspace_id[0], item_path)
        else:            
            if ".SemanticModel" in files:
                item_path = files.split(".SemanticModel")[0]+".SemanticModel"
            else:
                item_path = files.split(".Dataset")[0]+".Dataset/"
            print("Running semantic model deployment to path: " + item_path)
            it.simple_deploy_semantic_model(workspace_id[0], item_path)
    except Exception as e:
        print("Error_: ", e)
        raise Exception(e)

    
