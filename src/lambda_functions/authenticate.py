import json
import datetime
import random
import requests

def lambda_handler(event, context):
    
    date = datetime.datetime.utcnow().isoformat() # used https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python for utc iso date
    log_id = date + '-' + str(int(random.random()*1000000))
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/logging?documentId=" + log_id
    requests.post(url, data=json.dumps({"fields": {"event": {"stringValue" : json.dumps(event)}}}), timeout=60).json()
    
    return { 
        "statusCode": 501,
        "headers": {
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': '*',
        },
        "body": "No token"
    }
