# -*- coding: utf-8 -*-
"""
Código by ibarrau. La Data Web.

"""

import urllib.request as urllib2
import json
import pandas as pd
import sys
from datetime import datetime, date, timedelta

REST_API_URL = "[API POST Power Bi URL]"

if __name__ == '__main__':	

    try:        
        
        # Try BD connection to data
        try:
            ''' connecting data or BD '''
        except Exception as ex:
            print('Error en ', ex)
        
        # Read data frame from source
        ''' 
        df = pd.read_sql("QUERY", con = connection) 
		df = pd.read_csv(r"PATH", sep=",")
        
        '''
        
        
        # Transform Data
        ''' Here code to transform data '''
        
        #Convert Date to correct format and prepare the api body
        #df['fecha'] = [datetime.strftime(item, "%Y-%m-%dT%H:%M:%SZ") for item in df['fecha']]
        #df['fecha'] = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%SZ")
        
        # Prepare Power Bi API POST Body
		tiro = bytes(df.to_json(orient='records'), encoding='utf-8')
        
        # Power Bi API Post
        req = urllib2.Request(REST_API_URL, tiro)
        response = urllib2.urlopen(req)

        # Print result
        print("POST request to Power BI with data:{0}".format(tiro))
        print("Response: HTTP {0} {1}\n".format(response.getcode(), response.read()))		
			
    # Error Handling
    except urllib2.HTTPError as err:
        print(err.code)
        print(err)
    except Exception as ex:
        print("Sys ERROR: ", sys.exc_info()[0])
        print("Excepcion: ", ex)
                
    # Close DB connection
    ''' Here Close BD connection '''