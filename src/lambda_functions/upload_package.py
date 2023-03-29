import json
import requests

def lambda_handler(event, context):

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
    
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/acme-register-package-information?documentId=" + package_name

    response = requests.post(url, json.dumps(document)).json()

    return response