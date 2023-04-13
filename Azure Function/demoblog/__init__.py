import logging
from simplepbi import token
from simplepbi import groups
from simplepbi import utils
import json 
import azure.functions as func

TENANT_ID = 'e097d8d9-78e5-464a-888b-fe8bb8991200'
power_bi_client_id = '98d79e7b-e930-4fd0-a5ff-6c99acbaaad2'
power_bi_secret = 'cTT8Q~oMQhEhAdFIm46mFVZXHL9Y1XvfbtK7zb8J'

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        t = token.Token(TENANT_ID, power_bi_client_id, None, None, power_bi_secret, use_service_principal=True)
        g = groups.Groups(t.token)
        response = g.get_groups()
        #df = utils.to_pandas(response, "value")
        return func.HttpResponse(
            #json.dumps(df.to_dict(orient="records")),
            json.dumps(response),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(
            f"Request Accepted but the query to PBI API had an error when requesting the groups. Please contact your admin.", e.text, status_code=500
            )
