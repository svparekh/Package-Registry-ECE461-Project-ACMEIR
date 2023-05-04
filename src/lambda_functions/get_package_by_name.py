import json
import requests
import datetime
import random

def lambda_handler(event, context):
    
    date = datetime.datetime.utcnow().isoformat() # used https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python for utc iso date
    log_id = date + '-' + str(int(random.random()*1000000))
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/logging?documentId=" + log_id
    requests.post(url, data=json.dumps({"fields": {"event": {"stringValue" : json.dumps(event)}}}), timeout=60).json()

    package_name = event['path'][16:] # /package/byname/_______

    # see delete_package_by_name on links about query
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
                        "stringValue": package_name
                    }
                }
            }
        }
    }

    lookup_response = requests.post(url, json.dumps(request_body), timeout=60).json()

    if len(lookup_response) > 0 and 'document' in lookup_response[0].keys():
        history = []
        for document in lookup_response:
            url = "https://firestore.googleapis.com/v1/" + document['document']['name']
            response = requests.get(url, timeout=60).json()
            
            package_name = response['fields']['Name']['stringValue']
            package_version = response['fields']['Version']['stringValue']
            package_id = response['fields']['ID']['stringValue']
            history_entries = response['fields']['History']['arrayValue']['values']
            for entry in history_entries:
                history_entry = {
                    "User": {
                        "name": entry['mapValue']['fields']['User']['mapValue']['fields']['name']['stringValue'],
                        "isAdmin": entry['mapValue']['fields']['User']['mapValue']['fields']['isAdmin']['booleanValue']
                    },
                    "Date": entry['mapValue']['fields']['Date']['stringValue'],
                    "PackageMetadata": {
                        "Name": package_name,
                        "Version": package_version,
                        "ID": package_id
                    },
                    "Action": entry['mapValue']['fields']['Action']['stringValue']
                }
                history.append(history_entry)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                'Access-Control-Allow-Origin': '*',
            },
            "body": json.dumps(history)
        }
      
    return {
        "statusCode": 404,
        "headers": {
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': '*',
            },
        "body": "Package does not exist."
    }


