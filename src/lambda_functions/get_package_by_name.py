import json
import requests

def lambda_handler(event, context):
    
    package_name = event['path'][16:] # /packages/byname/_______
    
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/acme-register-package-information/" + package_name

    response = requests.get(url).json()
    
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