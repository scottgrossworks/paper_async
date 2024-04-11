##
## From the Document 'Asynchronous Messaging Design Pattern for AWS Lambda Services'
## 
##
## The Leedz
## theleedz.com
## theleedz.com@gmail.com
##
##
## This is the first approach at an asynchronous helper function -- in the doc this inevitably creates
## heavyweight spider legs with a lot of duplicate code.
##
## Step 2 of the document is to incorporate controllers which centralize the utility code and delegate to 
## notifyUsers in function calls, not separate lambda files
##
import json
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
    
    
    
##
## FUNCTION ENTRY POINT
##
## event -- will be Payload from calling Lambda function
##
def lambda_handler(event, context):

    logger.info(event)
    
    leed_id = validateParam(event, "id", 1)
    logger.info("THE LEED=" + leed_id)    
    
    trade = validateParam(event, "trade", 1)
    logger.info("TRADE=" + trade)
    
    seller = validateParam(event, "seller", 1)
    logger.info("SELLER=" + seller)
    
    
    ret_val = {
        'code':'success'
    }
    
    return json.dumps(ret_val)
    
    
    
    
    
    
    