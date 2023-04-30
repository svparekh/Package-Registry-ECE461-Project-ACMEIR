import json
import requests
import re
import datetime
import random

def lambda_handler(event, context):
  
    date = datetime.datetime.utcnow().isoformat() # used https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python for utc iso date
    log_id = date + '-' + str(int(random.random()*1000000))
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/logging?documentId=" + log_id
    requests.post(url, data=json.dumps({"fields": {"event": {"stringValue" : json.dumps(event)}}}), timeout=60).json()


    data = json.loads(event["body"])

    package_regex = data['RegEx']
    regex_compiled = re.compile(package_regex)

    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/"

    documents = requests.get(url, timeout=60).json()["documents"]
    
    matching_packages = []
    for document in documents:
        package_name = document['fields']['Name']['stringValue']
        package_version = document['fields']['Version']['stringValue']
        package_id = document['fields']['ID']['stringValue']

        if regex_compiled.match(package_name) != None:
            matching_packages.append({"Version" : package_version, "Name" : package_name, "ID" : package_id})

    did_find_packages = len(matching_packages) > 0
    if did_find_packages:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(matching_packages)
        }
    else:
        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "No package found under this regex."
        }
        
    