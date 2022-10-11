from simplepbi import token
from simplepbi import imports

# Parameters from Registered App and Workspace ID
TENANT_ID = ""
power_bi_client_id = "" 
power_bi_secret = ""
workspace_id = ""

# Create a token with Service Principal data
t = token.Token(TENANT_ID, power_bi_client_id, None, None, power_bi_secret, use_service_principal=True)

# Create import object to use its methods
im = imports.Imports(t.token)

# Call import by folder method example
im.simple_import_pbix_folder_in_group_preview(workspace_id, folderPath="C:/Users/SimplePBI/Documents/Area_Ventas/", nameConflict="CreateOrOverwrite")