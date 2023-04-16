import json
import requests

def lambda_handler(event, context):
    
  path_id = event['path'][9:]

  # NOTE: if it turns out we can't use proxy integration response to match the expected output, see upload-package
  # on using Exceptions instead. The exceptions also need to be set up in API Gateway

  url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/"+path_id
  response = requests.get(url).json()
  if not('error' in response):
    name = response['fields']['name']['stringValue']
    version = response['fields']['version']['stringValue']
    id = response['fields']['id']['stringValue']
    content = response['fields']['content']['stringValue']
    url = response['fields']['url']['stringValue']
    jsprogram = response['fields']['jsprogram']['stringValue']

    response_body = {
      "metadata": {
        "Name": name,
        "Version": version,
        "ID": id
      },
      "data": {
        "Content": content,
        "URL": url,
        "JSProgram": jsprogram
      }
    }

    proxy_integration_response = {
      "isBase64Encoded": False,
      "statusCode": 200,
      "headers": {},
      "body": json.dumps(response_body)
    }
    
    return proxy_integration_response
  
  proxy_integration_response = {
    "isBase64Encoded": False,
    "statusCode": 404,
    "headers": {},
    "body": "Failure - Package does not exist",
  }
      
  return proxy_integration_response
      