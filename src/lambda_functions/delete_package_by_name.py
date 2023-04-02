import json
import requests

def lambda_handler(event, context):
    
    package_name = event['path'][16:] # /package/byName/_______
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/name-to-id-lookup/" + package_name

    lookup_response = requests.get(url).json()
    delete_response = requests.delete(url).json()
    
    # NOTE: Assuming that acme-register-package-information and name-to-id-lookup are synced
    # SHOULD PROBABLY ADD ERROR CHECKING IF THAT IS NOT THE CASE

    if not("error" in lookup_response):
        for package_id in lookup_response['fields']:
            url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/acme-register-package-information/" + package_id
            delete_response = requests.delete(url).json()

        proxy_integration_response = {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {},
            "body": "Success - Package(s) deleted",
        }
    
        return proxy_integration_response
    
    proxy_integration_response = {
        "isBase64Encoded": False,
        "statusCode": 404,
        "headers": {},
        "body": "Failure - Package does not exist",
    }

    return proxy_integration_response