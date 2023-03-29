import json
import requests

def lambda_handler(event, context):
    
    # if ci/cd works, you should see this here

    path_id = event['path'][9:]
    
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/acme-register-package-information/"

    response = requests.get(url).json()
    
    documents = response['documents']
    
    # need to improve this - I'm assuming the id is in our database, if there's not, we need to return error. See bottom of function
    # also somewhere in the post package thing, we need to check if the ID already exists. We don't currently
    
    for document in documents:
      doc_id = document['fields']['package_id']['stringValue']
      if doc_id == path_id:
        package_name = document['fields']['package_name']['stringValue']
        package_version = document['fields']['package_version']['stringValue']
        package_id = document['fields']['package_id']['stringValue']
        package_content = document['fields']['package_content']['stringValue']
        package_url = document['fields']['package_url']['stringValue']
        package_jsprogram = document['fields']['package_jsprogram']['stringValue']
    
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
        
    return "error response should go here. Just copy proxy_integration_response but change body to the error from the OpenAPI spec. If you don't get what I'm saying don't worry about it I'll do after break"