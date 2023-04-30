import json
import requests
import re

def lambda_handler(event, context):
  
    data = json.loads(event["body"])

    package_regex = data['RegEx']
    regex_compiled = re.compile(package_regex)

    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/"

    documents = requests.get(url).json()["documents"]
    
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
                "Content-Type": "text/plain"
            },
            "body": "No package found under this regex."
        }
        
    