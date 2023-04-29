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
            url = "https://firestore.googleapis.com/v1/" + document["name"] # note that this isn't the 'name' field
            response = requests.delete(url).json()
            # https://cloud.google.com/storage/docs/json_api/v1/objects/delete
            url = "https://storage.googleapis.com/storage/v1/b/acme-register-contents/o/"+document["fields"]["ID"]['stringValue']
            response = requests.delete(url)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": "Registry is reset."
        })
    }