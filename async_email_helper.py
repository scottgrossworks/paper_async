##
## From the Document 'Asynchronous Messaging Design Pattern for AWS Lambda Services'
## 
##
## The Leedz
## theleedz.com
## theleedz.com@gmail.com
##
##
## Step 2 of the document incorporates ASYNC controllers like this helper function that composes and sends emails,
## DDB searches and other time-intensive activities and consolidates the utilities and handles involved in one file
##
##

# boto3 is our interface to other AWS services like DDB
import boto3
from boto3.dynamodb.conditions import Attr
from boto3.dynamodb.conditions import Key

import json

from datetime import datetime as dt, timezone

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)




    
    


## Helper functoin to extract incoming event parameters
## will throw ValueError
##
def validateParam( event, param, required ):
    
    value = ""
    
    if (param not in event):
            if required:
                raise ValueError("No '" + param + "' event parameter")
    else:
        value = event[param] 
        
    return value




 
 
#
# this helper function contains code serving several different callers
# the function name is in the event request object
# other params will vary accordingly
#
#
#
def lambda_handler(event, context):
    
    

    function_name = ""
    
    try:
        
        # VALIDATE ALL PARAMS
        #    
        function_name = validateParam(event, "function", 1)
        logger.info("FUNCTION=" + function_name)
        
        leed_id = validateParam(event, "id", 1)
        logger.info("THE LEED=" + leed_id)    
        
        trade = validateParam(event, "trade", 1)
        logger.info("TRADE=" + trade)
        
        seller = validateParam(event, "seller", 1)
        logger.info("SELLER=" + seller)

        
        #
        # obtain resource handles to pass into called functions
        #
        
        
        
        ##
        ## function name
        ##
        match function_name:
        
            # instead of a separate file we can pass any data this function needs as arguments in the same scope
            #
            case "notifyUsers":

                notifyUsers( leed_id, trade, seller)
               
            #
            # ... other functions ...
            #
                        
            # ERROR condition
            #
            case _:
                return handle_error("Unknown function request: " + function_name)
        
        
        # SUCCESS
        return handle_success("Mail handler invoked: " + function_name)
    
        
    except Exception as e:
        str_err = "Error calling async mail helper [" + function_name + "]: " + str(e)
        return handle_error( str_err )
    




## notifyUsers
## stub for a much larger function which might retrieve a list of users from DDB, filter them according to some criteria requiring another AWS Serice,
## compose an email and email the filtered list of users, all using shared utilites with other functions called from the lambda_handler above
##
def notifyUsers( leed_id, trade, seller ):

    logger.info("Notifying Users...")
    
    






# an EXAMPLE of a shared utility function that should not be repeated in every individual lambda file
# and you don't want to consolidate in a 'utility.py' that you call using the boto3 SDK because of the 
# marshalling/unmarshalling of JSON Payload and the fact you might be calling this a lot if you are 
# getting DB items and formatting them for emails
#
# convert a long date from now_milliseconds() into a pretty date
# January 05, 2024 - 11:29
#
def prettyDate( the_date ):
    
    if (not the_date) :
        return ""
    
    int_date = int(the_date)
    timestamp = dt.fromtimestamp( int_date / 1000)  # Convert milliseconds to seconds
    formatted_date = timestamp.strftime("%B %d, %Y - %H:%M")
    return formatted_date



# current time since epoch GMT (hopefully)
#
def now_milliseconds():
    current_time = dt.now(timezone.utc)
    epoch = dt(1970, 1, 1, tzinfo=timezone.utc)
    milliseconds_since_epoch = int((current_time - epoch).total_seconds() * 1000)
    return milliseconds_since_epoch

    
    
 
    


#
# pretty error return JSON
#
def handle_error( msg ):
  
    logger.error( msg )
    ret_obj = { "cd": 0,
                "err": msg
            }
    
    
    the_json = json.dumps(ret_obj)

    return the_json
    
    
    
    

#
# indicate success with a code and msg
#
def handle_success( msg ):
  
    ret_obj = { "cd": 1,
                "msg": msg
            }
    the_json = json.dumps(ret_obj)

    return the_json
    
    
    
    
    