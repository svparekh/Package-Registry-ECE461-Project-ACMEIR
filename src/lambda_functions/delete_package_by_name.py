import json
import requests

def lambda_handler(event, context):

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

    lookup_response = requests.post(url, json.dumps(request_body)).json()
    # print(lookup_response) # NOTE: IF I DONT WORK, CHECK THIS PRINT STATEMENT!!!
    
    if len(lookup_response) > 0 and 'document' in lookup_response[0].keys():
    
        for document in lookup_response:
            url = "https://firestore.googleapis.com/v1/" + document['document']['name']
            delete_response = requests.delete(url).json()

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "Package is deleted."
            })
        }
    
    return {
        "statusCode": 404,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "error": "Package does not exist."
        })
    }