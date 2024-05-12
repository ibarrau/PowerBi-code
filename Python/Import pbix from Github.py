
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
owner = "ibarrau"
repo = "PowerBi-code"
path = "PowerBi Reports/BlogDemos.pbix"
github_pat = "XXXX-XXX-XXX-XXX-XXXX"
workspace_id = "XXXX-XXX-XXX-XXX-XXXX"

# Request Github to import the file into the Power Bi delimited Workspace
im.simple_import_from_github(owner, repo, path, github_pat, workspace_id)