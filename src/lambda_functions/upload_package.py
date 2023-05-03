import json
import requests
import random
import datetime

def lambda_handler(event, context):
    
    date = datetime.datetime.utcnow().isoformat() # used https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python for utc iso date
    log_id = date + '-' + str(int(random.random()*1000000))
    # https://cloud.google.com/storage/docs/uploading-objects#rest-upload-objects
    url = "https://storage.googleapis.com/upload/storage/v1/b/acme-register-logging/o?uploadType=media&name="+log_id
    # https://www.w3schools.com/python/ref_requests_post.asp
    requests.post(url, data=json.dumps(event), timeout=60)

    data = json.loads(event["body"])

    package_content = data.get("Content", "notFound")
    package_url = data.get("URL", "notFound")
    package_jsprogram = data.get("JSProgram", "notFound")
    
    if package_content == None:   package_content = "notFound"
    if package_url == None:       package_url = "notFound"
    if package_jsprogram == None: package_jsprogram = "notFound"
    
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
    
    response = requests.post(url, data=json.dumps(request_body), headers=headers, timeout=60).json()

    if "Package exists already." in response.keys():
        return {
            "statusCode": 409,
            "headers": {
                "Content-Type": "application/json",
                'Access-Control-Allow-Origin': '*',
            },
            "body": "Package exists already."
        }

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
          "Content-Type": "application/json",
          'Access-Control-Allow-Origin': '*',
      },
      "body": json.dumps(response)
    }

            
    


    
    

    

