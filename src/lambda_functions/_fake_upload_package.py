import json
import requests
import random

def lambda_handler(event, context):

    # NOTE: seems like in current API we do not have access to name, version, or id.
    # So these are currently here for simple testing but probably need to be deleted soon.
    package_name = event["metadata"]["Name"]
    package_version = event["metadata"]["Version"]
    package_id = event["metadata"]["ID"]
    
    package_content = event["data"].get("Content", "notFound")
    package_url = event["data"].get("URL", "notFound")
    package_jsprogram = event["data"].get("JSProgram", "notFound")
    
    # package ingest
    #if package_url != "notFound":
        # scrape NPM page for github URL
        # run other group's scorer function on github to get metrics - if all are > 0.5, proceed

    # NOTE : for both this and rate, we're going to have to run something computationally expensive, 
    # either running the other groups ridiculous multithreading stuff or decoding base64, etc. Because
    # I personally get charged for the GB seconds we use in these Lambda functions, I'd much rather we
    # set up an API call to a Cloud Compute function in Google Cloud Platform or something. Gotta get my
    # money's use of these credits
    
    # TODO: need to add error code return for bad rating



    # TODO: We need to decide what is consistent between packages and what to query for to verify whether or not a package
    # already exists. This is because there is not a package_id inputted like it used to be, so we can't use that to check.
    # Below is slightly-updated old code, but the get with package_id and the conditionals on the ifs are going to need to 
    # change.  

    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/" + package_id
    response = requests.get(url).json()
    # print(response)
    
    if not("error" in response):
        # id already exists
        if response["fields"]['package_name']['stringValue'] == package_name and response["fields"]['package_version']['stringValue'] == package_version:
            # package already exists
            
            raise Exception("Invalid.Package_exists_already")
            
            # proxy_integration_response = { 
            #     "isBase64Encoded": False,
            #     "statusCode": 409,
            #     "headers": {},
            #     "body": json.dumps(response_body)
            # }
            
            # return proxy_integration_response
        else:
            # package does not exist
             
            # while not('error' in response): # this makes me scared
            for i in range(10): # WARNING: will break database if can't find unused number in 10 tries
                if "error" in response: break
                package_id = str(random.randint(1000, 999999999)) # is this enough numbers?
                url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/" + package_id
                response = requests.get(url).json()
            

    # TODO: The fields/names should be probably be changed and then synchronized with other files
    document = {
        "fields" : {
            "package_name" : {
                "stringValue" : package_name
            },
            "package_version" : {
                "stringValue" : package_version
            },
            "package_id" : {
                "stringValue" : package_id
            },
            "package_content" : {
                "stringValue" : package_content
            },
            "package_url" : {
                "stringValue" : package_url
            },
            "package_jsprogram" : {
                "stringValue" : package_jsprogram
            }
        }
    } 

    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages?documentId=" + package_id
    response = requests.post(url, json.dumps(document)).json()
    
    response_body = { # from get-package
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
    
    return response_body
    
    # proxy_integration_response = { # from get-package
    #     "isBase64Encoded": False,
    #     "statusCode": 201,
    #     "headers": {},
    #     "body": json.dumps(response_body)
    # }
    
    # return proxy_integration_response

