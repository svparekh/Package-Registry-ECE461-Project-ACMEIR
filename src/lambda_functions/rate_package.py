import json
import requests
import datetime
import random

def lambda_handler(event, context):

    date = datetime.datetime.utcnow().isoformat() # used https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python for utc iso date
    log_id = date + '-' + str(int(random.random()*1000000))
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/logging?documentId=" + log_id
    requests.post(url, data=json.dumps({"fields": {"event": {"stringValue" : json.dumps(event)}}}), timeout=60).json()


    package_id = event['path'][9:][:-5]
    
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/" + package_id
    
    response = requests.get(url, timeout=60).json()
    
    if "error" in response:
    
        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json",
                'Access-Control-Allow-Origin': '*',
            },
            "body": "Package does not exist."
        }

    responsive_maintainer_score = response['fields']['ResponsiveMaintainerScore']['stringValue']
    ramp_up_score = response['fields']['RampUpScore']['stringValue']
    bus_factor_score = response['fields']['BusFactorScore']['stringValue']
    fraction_reviewed_score = response['fields']['FractionReviewedScore']['stringValue']
    fraction_dependencies_score = response['fields']['FractionDependenciesScore']['stringValue']
    license_score = response['fields']['LicenseScore']['stringValue']
    correctness_score = response['fields']['CorrectnessScore']['stringValue']
    net_score = response['fields']['NetScore']['stringValue']
    
    scores = {
        "BusFactor": bus_factor_score,
        "Correctness": correctness_score,
        "RampUp": ramp_up_score,
        "ResponsiveMaintainer": responsive_maintainer_score,
        "LicenseScore": license_score,
        "GoodPinningPractice": fraction_dependencies_score,
        "PullRequest": fraction_reviewed_score,
        "NetScore": net_score
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': '*',
        },
        "body": json.dumps(scores)
    }
