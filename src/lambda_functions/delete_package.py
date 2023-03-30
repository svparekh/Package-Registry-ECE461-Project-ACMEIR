import json
import requests

def lambda_handler(event, context):
    
  path_id = event['path'][9:]
  
  url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/acme-register-package-information/" + path_id
  package = requests.get(url).json()
  
  if not("error" in package):
    delete_response = requests.delete(url).json()

    doc_name = package['fields']['package_name']['stringValue']
    
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/name-to-id-lookup/" + doc_name
    response = requests.get(url).json()

    # NOTE: Assuming that acme-register-package-information and name-to-id-lookup are synced
    # SHOULD PROBABLY ADD ERROR CHECKING IF THAT IS NOT THE CASE

    delete_response = requests.delete(url).json()
    
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/name-to-id-lookup?documentId=" + doc_name
    
    response['fields'].pop(path_id)
    response.pop("name")
    if len(response['fields'].keys()) != 0:
      response = requests.post(url, json.dumps(response)).json()
      print(response)

    proxy_integration_response = {
      "isBase64Encoded": False,
      "statusCode": 200,
      "headers": {},
      "body": "Success - Package is deleted",
    }
    
    return proxy_integration_response
      
  proxy_integration_response = {
    "isBase64Encoded": False,
    "statusCode": 404,
    "headers": {},
    "body": "Failure - Package does not exist",
  }

  return proxy_integration_response