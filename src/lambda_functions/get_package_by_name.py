import json
import requests

def lambda_handler(event, context):
  
  package_name = event['path'][16:] # /package/byname/_______

  # TODO: NEED TO ADD USER, DATE, AND ACTION TO PACKAGE HISTORY ENTRIES!

  url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/name-to-id-lookup/" + package_name

  lookup_response = requests.get(url).json()

  if not("error" in lookup_response):
    history = []
    for package_id in lookup_response['fields']:
      url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/acme-register-package-information/" + package_id
      response = requests.get(url).json()
      
      package_name = response['fields']['package_name']['stringValue']
      package_version = response['fields']['package_version']['stringValue']
      package_id = response['fields']['package_id']['stringValue']
      
      history_entry = {
        "metadata": {
          "Name": package_name,
          "Version": package_version,
          "ID": package_id
        }
      }
      history.append(history_entry)


    proxy_integration_response = {
      "isBase64Encoded": False,
      "statusCode": 200,
      "headers": {},
      "body": history,
    }

    return proxy_integration_response
  
  proxy_integration_response = {
    "isBase64Encoded": False,
    "statusCode": 404,
    "headers": {},
    "body": "Failure - Package does not exist",
  }

  return proxy_integration_response








  url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/acme-register-package-information/" + package_name

  response = requests.get(url).json()
  
  