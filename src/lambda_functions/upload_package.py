import json
import requests
import random
import datetime

def lambda_handler(event, context):
    
    data = json.loads(event["body"])

    package_content = data.get("Content", "notFound")
    package_url = data.get("URL", "notFound")
    package_jsprogram = data.get("JSProgram", "notFound")
    
    # both are set or both are not set - return error
    if (package_url != "notFound" and package_content != "notFound") or (package_url == "notFound" and package_content == "notFound"):
        return {
          "statusCode": 400,
          "headers": {
              "Content-Type": "application/json"
          },
          "body": "There is missing field(s) in the PackageData/AuthenticationToken or it is formed improperly (e.g. Content and URL are both set), or the AuthenticationToken is invalid."
        }
    
    # package url is set
    if package_url != "notFound":
        payload = package_url
    else:
        payload = package_content
        
    
    url = "https://us-central1-acme-register.cloudfunctions.net/ssh"
    
    request_body = {
        "Content" : payload,
        "JSProgram" : package_jsprogram
    }
    
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, data=json.dumps(request_body), headers=headers).json()
    
    package_id = response['fields']['ID']['stringValue']
    name = response['fields']['Name']['stringValue']
    jsprogram = response['fields']['JSProgram']['stringValue']
    content = response['fields']['Content']['stringValue']
    version = response['fields']['Version']['stringValue']
    
    response = {
        "metadata" : {
            "Name" : name,
            "Version" : version,
            "ID" : package_id,
        },
        "data" : {
            "Content" : content,
            "JSProgram" : jsprogram,
        }
    }
    
    return {
      "statusCode": 201,
      "headers": {
          "Content-Type": "application/json"
      },
      "body": json.dumps(response)
    }

            
    


    
    

    

