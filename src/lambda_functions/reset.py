import json
import requests
import datetime
import random

def lambda_handler(event, context):
    
    date = datetime.datetime.utcnow().isoformat() # used https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python for utc iso date
    id = date + '-' + str(int(random.random()*1000000))
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/logging?documentId=" + id
    response = requests.post(url, data=json.dumps({"fields": {"event": {"stringValue" : json.dumps(event)}}})).json()


    # This was copied and edited from delete-package and referenced get-package
    
    # NEED TO SET UP PROPER RESPONSES

    # ALSO THIS IS REALLY SLOW
    
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/"

    response = requests.get(url).json()
    
    if 'documents' in response.keys():
        documents = response['documents']
        
        for document in documents:
            url = "https://firestore.googleapis.com/v1/" + document["name"] # note that this isn't the 'name' field
            response = requests.delete(url).json()
            # https://cloud.google.com/storage/docs/json_api/v1/objects/delete
            url = "https://storage.googleapis.com/storage/v1/b/acme-register-contents/o/"+document["fields"]["ID"]['stringValue']
            response = requests.delete(url)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "Registry is reset."
    }