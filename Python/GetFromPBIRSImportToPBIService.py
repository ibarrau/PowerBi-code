import requests
import json
from requests_ntlm2 import HttpNtlmAuth
from simplepbi import token
from simplepbi import imports

if __name__ == '__main__':	

    # Prepare credentials and URL for PBIRS 
    username = ""
    password = ""
    # You can get the report_id from the UI or request content from a Folder
    report_id = "2a0575c7-27de-48c8-9fa7-9d0d362f7b61"    
    baseurl = 'http://localhost/Reports/api/v2.0/'
    
    # Get Nltm Auth in order to validate login on requests
    auth=HttpNtlmAuth(username,password)
    print("Getting report name from id...")
    # Make get request to obtain the name of the report id
    report_name = requests.get(baseurl+'PowerBIReports('+report_id+')',auth=auth).json()["Name"] + '.pbix'
    print("Getting report", report_name, "...")
    # Make get request to obtain the file from report server
    result = requests.get(baseurl + 'PowerBIReports('+report_id+')/Content/$value' ),auth=auth)    
    
    # Power Bi Service params to login
    TENANT_ID = ""
    power_bi_client_id = '' 
    power_bi_secret = ''
    workspace_id = ''
    
    # Get Embed token
    t = token.Token(TENANT_ID, power_bi_client_id, None, None, power_bi_secret, use_service_principal=True)
    # Create import object
    im = imports.Imports(t.token)
    # Importing report to a selected workspace with its name
    im.simple_import_pbix_as_parameter(workspace_id, result.content, report_name)
   