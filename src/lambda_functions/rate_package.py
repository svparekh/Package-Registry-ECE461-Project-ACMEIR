import json
import requests

def lambda_handler(event, context):

    package_id = event['path'][9:][:-5]
    
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/" + package_id
    
    response = requests.get(url).json()
    
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
          "Content-Type": "application/json"
      },
      "body": json.dumps(scores)
    }
