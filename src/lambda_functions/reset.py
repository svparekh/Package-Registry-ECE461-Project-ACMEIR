import json
import requests

def lambda_handler(event, context):
    
    # This was copied and edited from delete-package and referenced get-package
    
    # NEED TO SET UP PROPER RESPONSES

    # ALSO THIS IS REALLY SLOW
    
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/"

    response = requests.get(url).json()
    
    if 'documents' in response.keys():
        documents = response['documents']
        
        for document in documents:
            url = "https://firestore.googleapis.com/v1/" + document["name"]
            response = requests.delete(url).json()

    proxy_integration_response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": "success - something informative should go here",
    }
    
    return proxy_integration_response