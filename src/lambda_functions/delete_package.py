import json
import requests
import datetime
import random

def lambda_handler(event, context):
    
    date = datetime.datetime.utcnow().isoformat() # used https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python for utc iso date
    log_id = date + '-' + str(int(random.random()*1000000))
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/logging?documentId=" + log_id
    requests.post(url, data=json.dumps({"fields": {"event": {"stringValue" : json.dumps(event)}}}), timeout=60).json()

    path_id = event['path'][9:]
    
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/" + path_id
    
    response = requests.get(url, timeout=60).json() 

    requests.delete(url, timeout=60).json()

    if not("error" in response):

        # https://cloud.google.com/storage/docs/json_api/v1/objects/delete
        url = "https://storage.googleapis.com/storage/v1/b/acme-register-contents/o/"+path_id
        response = requests.delete(url, timeout=60)
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                'Access-Control-Allow-Origin': '*',
            },
            "body": "Package is deleted."
        }
        
    return {
        "statusCode": 404,
        "headers": {
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': '*',
        },
        "body": "Package does not exist."
    }