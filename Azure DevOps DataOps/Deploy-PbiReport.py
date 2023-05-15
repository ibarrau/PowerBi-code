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
from simplepbi import token
from simplepbi import imports

# Set variables
Throw_exception = ""
Folder_Name = sys.argv[1]
Workspace = sys.argv[2]
Files = " ".join(sys.argv[3:])
print("The arguments are: " , str(sys.argv))

print("Folder_Name: " + Folder_Name, "\nWorkspace: " + Workspace, "\nFiles: " + Files)

# Get list of files to import
list_files = [item for item in Files.split(",") if item[-4:]=="pbix" and item.split("/")[0] ==Folder_Name]
print("list_files: " + str(list_files))

# log into Power BI
TENANT_ID = os.environ.get("AZURE_TENANT_ID")
power_bi_client_id = os.environ.get("AZURE_CLIENT_ID")
power_bi_secret = os.environ.get("AZURE_CLIENT_SECRET")
print("Environment Variables loaded.")

# get token and create objects
t = token.Token(TENANT_ID, power_bi_client_id, None, None, power_bi_secret, use_service_principal=True)
im = imports.Imports(t.token)

print("Token generated")

for file in list_files:
    # import report from path
    try:
        print("Importing ", file, "into workspace id ", Workspace, " from folder ", Folder_Name, "...")
        res = im.simple_import_pbix_in_group(workspace_id=Workspace, filePath=file, datasetDisplayName=file.split("/")[1], nameConflict="CreateOrOverwrite")
        if res.status_code == 202:
            print("File imported: " + file)
        else:
            print("Error importing file: " + file)
            print(res.text)
            Throw_exception = Throw_exception + "Error importing file: " + file + ".\n"
            pass
    except:
        print("Error importing file: " + file)
        Throw_exception = Throw_exception + "Error importing file: " + file + ".\n"
        pass

if Throw_exception != "":
    raise Exception(Throw_exception)