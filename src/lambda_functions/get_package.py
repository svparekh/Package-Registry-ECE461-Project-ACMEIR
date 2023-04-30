import json
import requests
import datetime
import random

def lambda_handler(event, context):

    date = datetime.datetime.utcnow().isoformat() # used https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python for utc iso date
    id = date + '-' + str(int(random.random()*1000000))
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/logging?documentId=" + id
    response = requests.post(url, data=json.dumps({"fields": {"event": {"stringValue" : json.dumps(event)}}})).json()


    path_id = event['path'][9:]

    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/"+path_id
    document = requests.get(url).json()
    if not 'error' in document:
        name = document['fields']['Name']['stringValue']
        version = document['fields']['Version']['stringValue']
        id = path_id

        # https://cloud.google.com/storage/docs/json_api/v1/objects/get#http-request
        # https://cloud.google.com/storage/docs/json_api#query_parameters
        url = "https://storage.googleapis.com/storage/v1/b/acme-register-contents/o/"+path_id+"?alt=media"

        # https://www.w3schools.com/python/ref_requests_response.asp
        content_document = requests.get(url)
        if not content_document.ok :
            return { 
                "statusCode": 404,
                "headers": {
                    "Content-Type": "test/plain"
                },
                "body": "Package does not exist."
            }

        response_body = {
            "metadata": {
                "Name": name,
                "Version": version,
                "ID": id
            },
            "data": {
                "Content": content_document.text
            }
        }

        # used https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python for utc iso date
        date = datetime.datetime.utcnow().isoformat()
        date = date[0:date.index('.')]+'Z'

        history_entry = {
            'mapValue': {
                'fields': {
                    'Action': {
                        'stringValue': 'DOWNLOAD'
                    },
                    'User': {
                        'mapValue': {
                            'fields': {
                                'name': {
                                    'stringValue': 'UNIMPLEMENTED'
                                }, 
                                'isAdmin': {
                                    'booleanValue': True
                                }
                            }
                        }
                    }, 
                    'Date': {
                        'stringValue': date
                    }
                }
            }
        }

        document['fields']['History']['arrayValue']['values'].append(history_entry)

        document.pop('name') # NOT the name field; necessary to remove for posting

        # print(document, end="\n\n\n")

        url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/" + id
        response = requests.delete(url).json() # unchecked
        # print(response, end="\n\n\n")

        url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages?documentId=" + id
        response = requests.post(url, json.dumps(document)).json()
        # print(response, end="\n\n\n")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(response_body)
        }

    return { 
        "statusCode": 404,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "Package does not exist."
    }