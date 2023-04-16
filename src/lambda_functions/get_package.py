import json
import requests
import datetime

def lambda_handler(event, context):
    
  path_id = event['path'][9:]

  # NOTE: if it turns out we can't use proxy integration response to match the expected output, see upload-package
  # on using Exceptions instead. The exceptions also need to be set up in API Gateway

  url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/"+path_id
  document = requests.get(url).json()
  if not('error' in document):
    name = document['fields']['name']['stringValue']
    version = document['fields']['version']['stringValue']
    id = document['fields']['id']['stringValue']
    content = document['fields']['content']['stringValue']
    url = document['fields']['url']['stringValue']
    jsprogram = document['fields']['jsprogram']['stringValue']

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


    # used https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python for utc iso date
    date = datetime.datetime.utcnow().isoformat()
    date = date[0:date.index('.')]+'Z'

    history_entry = {
        'mapValue': {
            'fields': {
                'Action': {
                    'stringValue': 'DOWNLOAD'
                }, 
                'User': {
                    'mapValue': {
                        'fields': {
                            'name': {
                                'stringValue': 'UNIMPLEMENTED'
                            }, 
                            'isAdmin': {
                                'booleanValue': True
                            }
                        }
                    }
                }, 
                'Date': {
                    'stringValue': date
                }
            }
        }
    }

    document['fields']['history']['arrayValue']['values'].append(history_entry)

    document.pop('name') # NOT the name field; necessary to remove for posting

    # print(document, end="\n\n\n")

    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/" + id
    response = requests.delete(url).json() # unchecked
    # print(response, end="\n\n\n")
        
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages?documentId=" + id
    response = requests.post(url, json.dumps(document)).json()
    # print(response, end="\n\n\n")



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
      