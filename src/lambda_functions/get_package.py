import json
import requests

def lambda_handler(event, context):
    
  path_id = event['path'][9:]

  # NOTE: if it turns out we can't use proxy integration response to match the expected output, see upload-package
  # on using Exceptions instead. The exceptions also need to be set up in API Gateway

  url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/acme-register-package-information/"+path_id
  response = requests.get(url).json()
  if not('error' in response):
    package_name = response['fields']['package_name']['stringValue']
    package_version = response['fields']['package_version']['stringValue']
    package_id = response['fields']['package_id']['stringValue']
    package_content = response['fields']['package_content']['stringValue']
    package_url = response['fields']['package_url']['stringValue']
    package_jsprogram = response['fields']['package_jsprogram']['stringValue']

    response_body = {
      "metadata": {
        "Name": package_name,
        "Version": package_version,
        "ID": package_id
      },
      "data": {
        "Content": package_content,
        "URL": package_url,
        "JSProgram": package_jsprogram
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
      