# Import necessary classes from library
from simplepbi import token
from simplepbi import imports

# Set PBI Rest API auth variables
TENANT_ID = "XXXX-XXX-XXX-XXX-XXXX"
power_bi_client_id = 'XXXX-XXX-XXX-XXX-XXXX' 
power_bi_secret = 'XXXX-XXX-XXX-XXX-XXXX'

# Get Token and creat import category object
t = token.Token(TENANT_ID, power_bi_client_id, None, None, power_bi_secret, use_service_principal=True)
im = imports.Imports(t.token)

# Set Repo Variables
organization = "ibarrau"
project = "ladataweb_proj"
repository_id = "ladataweb_proj"
path = "/Blogging/Admin - Activity Logs.pbix"
devopsKey = "XXXX-XXX-XXX-XXX-XXXX"
workspace_id = "XXXX-XXX-XXX-XXX-XXXX"

# Request DevOps to import the file into the Power Bi delimited Workspace
im.simple_import_from_devops(organization, project, repository_id, path, devopsKey, workspace_id)