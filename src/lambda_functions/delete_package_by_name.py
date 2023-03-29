import json
import requests

def lambda_handler(event, context):
    
    package_name = event['path'][16:] # /packages/byname/_______
    
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/acme-register-package-information/" + package_name

    response = requests.delete(url).json()
    
    proxy_integration_response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": "mission accomplished, i hope"
    }
    
    return proxy_integration_response