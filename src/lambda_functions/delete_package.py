import json
import requests

def lambda_handler(event, context):
    
  path_id = event['path'][9:]
  
  url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/" + path_id
  
  response = requests.get(url).json() 

  delete_response = requests.delete(url).json()

  # print(response)

  if not("error" in response):

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