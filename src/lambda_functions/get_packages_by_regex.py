import json
import requests
import re

def lambda_handler(event, context):
  
    package_regex = event['RegEx']

    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/"

    documents = requests.get(url).json()
    
    matching_packages = []
    for document in documents:
        package_name = document['fields']['name']['stringValue']
        package_version = document['fields']['version']['stringValue']
        package_id = document['fields']['id']['stringValue']

        if nameMatchesRegex(package_name, package_regex):
            matching_packages.append({"Name" : package_name, "Version" : package_version, "ID" : package_id})

    proxy_integration_response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(matching_packages),
    }

    return proxy_integration_response
  

def nameMatchesRegex(name, regex):
    expression = re.compile(regex)
    return expression.match(name) != None