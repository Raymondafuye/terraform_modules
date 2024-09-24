from validate_resend_verify_code import validate_input
from uuid import uuid4
import logging
import boto3
from time import time
from os import getenv
import os

cognito_client = boto3.client("cognito-idp")
CLIENT_ID = os.environ["CLIENT_ID"]

if logging.getLogger().hasHandlers():
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()


def lambda_handler(event, context):
    status_code = 400
    logger.info(event)
    resp = {
        "status": "error",
        "message": "server error",
        "data": None
    }
    try:
        payload = event.get("body")
        validate_input(payload)
        
        event = event.get("body") 
        username = event['email']
        response = cognito_client.resend_confirmation_code(
            ClientId=CLIENT_ID,
            Username=username,
        )
        
    except ValueError as e:
        logger.error(e)
        resp["message"] = str(e)
    except Exception as e:
        status_code = 500
        logger.error(e)
        resp["message"] = str(e)
    

    return make_response(status_code, resp)
 
    
####################################################################
#### HELPER FUNCTIONS
#-------------------------

def make_response(status, message, log=True):
    if log:
        logger.info(f"Response: status-{status}, body-{message}")
    return {
        "statusCode": status,
        "body": message
    }
