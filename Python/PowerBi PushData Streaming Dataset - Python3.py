
import urllib.request as urllib2
import json
import pandas as pd
from datetime import datetime, date, timedelta

def post_data_powerbi_setreaming_dataset(API_POST_URL):
    try:              
        # Get Data from source to push in Power Bi with any pd.read_XXX pandas connection.
        df = pd.read_sql("SELECT * FROM ... ", con = connection) 
        
        # Start of transformations and merging here
        # 
        #
        # End of transformations and merging here
        
        
        # In case you have dates. Convert Date to correct format and prepare the api body
        df['date'] = [datetime.strftime(item, "%Y-%m-%dT%H:%M:%SZ") for item in df['fecha']]
        
        # In case you want the insert date of the streaming 
        df['push_date'] = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%SZ")
        
        # Prepare the body creating a bytes array
        body = bytes(df.to_json(orient='records'), encoding='utf-8')
        
        #API Post
        req = urllib2.Request(REST_API_URL, body)
        response = urllib2.urlopen(req)

        #Print result
        print("POST request to Power BI with data:{0}".format(body))
        print("Response: HTTP {0} {1}\n".format(response.getcode(), response.read()))		
			
    except urllib2.HTTPError as err:
        print("Error Code is: ", err.code)
        print("Message ERROR is: ", err)
    except Exception as ex:
        print("Sys ERROR: ", sys.exc_info()[0])
        print("Excepcion: ", ex)
        
       
# If you want to run it with this file in a VM you can use this.        
if __name__ == '__main__':	
    
    REST_API_URL = "[API POST Power Bi URL]"
    post_data_powerbi_setreaming_dataset(REST_API_URL)
    
    