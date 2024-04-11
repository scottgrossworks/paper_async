##
## From the Document 'Asynchronous Messaging Design Pattern for AWS Lambda Services'
## 
##
## The Leedz
## theleedz.com
## theleedz.com@gmail.com
##
##
## Step 1 approach uses mutliple asynchronous helper functions -- in the doc this inevitably creates
## heavyweight spider legs with a lot of duplicate code.
##
## Step 2 of the document is to incorporate controllers which centralize the utility code and delegate to 
## notifyUsers in function calls, not separate lambda files
##
## see async_email_helper.py
##



import json
import boto3
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

    return value
    
    
    
    

##
## main entry-point into the function
##
def lambda_handler(event, context):


    func_args = {
        'id':'0123456789',
        'trade':'caricatures',
        'seller':'scott.gross'
    }

    # asynchronous
    lambda_function = boto3.client('lambda')
    lambda_function.invoke( FunctionName='notifyUsers',
                            InvocationType='RequestResponse',
                            Payload= json.dumps( func_args ) )


    
    #
    # the change below calls the controller and passes in the function name
    # in the Payload
    #
    '''
    payload = {
        'function':'notifyUsers',
        'id': '123456789',
        'trade': 'caricatures',
        'seller': 'scott.gross'
    }

    lambda_function = boto3.client('lambda')
    lambda_function.invoke(FunctionName='async_email_helper',
    InvocationType='Event',
    Payload= json.dumps( payload ))
    '''
    