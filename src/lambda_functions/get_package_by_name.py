import json
import requests

def lambda_handler(event, context):
  
  package_name = event['path'][16:] # /package/byname/_______

  # TODO: NEED TO ADD USER, DATE, AND ACTION TO PACKAGE HISTORY ENTRIES!

  # see delete_package_by_name on links about query
  url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents:runQuery"
  request_body = {
    "structuredQuery": {
        "from": [{
            "collectionId": "packages",
            "allDescendants": True
        }],
        "where": {
            "fieldFilter": {
                "field": {
                    "fieldPath": "package_name"
                },
                "op": "EQUAL",
                "value": {
                    "stringValue": package_name
                }
            }
        }
    }
  }

  lookup_response = requests.post(url, json.dumps(request_body)).json()

  if len(lookup_response) > 0 and 'document' in lookup_response[0].keys():
    history = []
    for document in lookup_response:
      url = "https://firestore.googleapis.com/v1/" + document['document']['name']
      response = requests.get(url).json()
      
      package_name = response['fields']['package_name']['stringValue']
      package_version = response['fields']['package_version']['stringValue']
      package_id = response['fields']['package_id']['stringValue']
      
      history_entry = {
        "User": {
          "name": "UNIMPLEMENTED",
          "isAdmin": True
        },
        "Date": "UNIMPLEMENTED",
        "PackageMetadata": {
          "Name": package_name,
          "Version": package_version,
          "ID": package_id
        },
        "Action": "UNIMPLEMENTED"
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
