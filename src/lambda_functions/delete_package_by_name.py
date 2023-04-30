import json
import requests
import datetime
import random

def lambda_handler(event, context):

    date = datetime.datetime.utcnow().isoformat() # used https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python for utc iso date
    log_id = date + '-' + str(int(random.random()*1000000))
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/logging?documentId=" + log_id
    requests.post(url, data=json.dumps({"fields": {"event": {"stringValue" : json.dumps(event)}}}), timeout=60).json()

    name = event['path'][16:] # /package/byName/_______

    #  url and request from https://stackoverflow.com/questions/60486537/firebase-firestore-rest-request-query-and-filter
    # also looked at https://stackoverflow.com/questions/66262701/only-structured-queries-are-supported-firestore-api-rest
    # used documentation https://cloud.google.com/firestore/docs/reference/rest/v1beta1/projects.databases.documents/runQuery and connected links
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents:runQuery"
    request_body = {
        "structuredQuery": {
            "from": [{
                "collectionId": "packages",
                "allDescendants": True
            }],
            "where": {
                "fieldFilter": {
                    "field": {
                        "fieldPath": "Name"
                    },
                    "op": "EQUAL",
                    "value": {
                        "stringValue": name
                    }
                }
            }
        }
    }

    lookup_response = requests.post(url, json.dumps(request_body), timeout=60).json()
    # print(lookup_response) # NOTE: IF I DONT WORK, CHECK THIS PRINT STATEMENT!!!
    
    if len(lookup_response) > 0 and 'document' in lookup_response[0].keys():
    
        for document in lookup_response:
            print(document)
            url = "https://firestore.googleapis.com/v1/" + document['document']['name']
            requests.delete(url, timeout=60).json()
            # https://cloud.google.com/storage/docs/json_api/v1/objects/delete
            url = "https://storage.googleapis.com/storage/v1/b/acme-register-contents/o/"+document['document']["fields"]["ID"]['stringValue']
            requests.delete(url, timeout=60)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "Package is deleted."
        }
    
    return {
        "statusCode": 404,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "Package does not exist."
    }