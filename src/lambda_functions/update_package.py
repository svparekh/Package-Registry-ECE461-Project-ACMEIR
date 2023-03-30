import json
import requests

def lambda_handler(event, context):
    #Chase: 
    # Needs to be implemented. I'm holding off for now because this will be very similar to uploading a package, and I think there's a few changes we need
    # to make first (returning right status code according to the spec, checking to see if id exists, handling duplicate names, etc.)
    
    # David:
    # I'm going to do it somewhat just so I can check it off the plan lol

    package_name = event["metadata"]["Name"]
    package_version = event["metadata"]["Version"]
    package_id = event["metadata"]["ID"]
    
    package_content = event["data"].get("Content", "notFound")
    package_url = event["data"].get("URL", "notFound")
    package_jsprogram = event["data"].get("JSProgram", "notFound")
    
    # NOTE: I'm assuming that we don't rate the package on update because there is no error code for it
    
    # TODO: check that the id passed in to the call and the one in the metadata is the same

    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/acme-register-package-information/" + package_id
    response = requests.get(url).json()
    
    if "error" in response or response["fields"]['package_name']['stringValue'] != package_name or response["fields"]['package_version']['stringValue'] != package_version:
            
            response_body = { # IS THE DESCRIPTION SOMETHING THAT GOES INTO THE RESPONSE?
                "description": "Package does not exist."
            }
            
            raise Exception("Invalid.Package_does_not_exist")
            
            # proxy_integration_response = { 
            #     "isBase64Encoded": False,
            #     "statusCode": 404,
            #     "headers": {},
            #     "body": json.dumps(response_body)
            # }
            
            # return proxy_integration_response

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

    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/acme-register-package-information/" + package_id
    response = requests.delete(url).json() # unchecked
        
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/acme-register-package-information?documentId=" + package_id
    response = requests.post(url, json.dumps(document)).json()
    
    response_body = { # IS THE DESCRIPTION SOMETHING THAT GOES INTO THE RESPONSE?
        "description": "Version is updated."
    }
    
    # proxy_integration_response = { 
    #     "isBase64Encoded": False,
    #     "statusCode": 200,
    #     "headers": {},
    #     "body": json.dumps(response_body)
    # }
    
    return #proxy_integration_response