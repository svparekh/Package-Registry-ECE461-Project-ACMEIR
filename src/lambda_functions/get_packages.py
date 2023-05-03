import json
import requests
import datetime
import random

def lambda_handler(event, context):

    date = datetime.datetime.utcnow().isoformat() # used https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python for utc iso date
    log_id = date + '-' + str(int(random.random()*1000000))
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/logging?documentId=" + log_id
    requests.post(url, data=json.dumps({"fields": {"event": {"stringValue" : json.dumps(event)}}}), timeout=60).json()

    # Needs to be tested extensively. I've tested a decent amount, but there's like 100 possible test cases. I
    # might make a generate test case  script 
    
    # get packages
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/"
    response = requests.get(url, timeout=60).json()
    packages = response['documents']
    
    # establish name->version dictionary
    name_to_version = {} # {name1: [(version1, id1), (version2, id2)]}
    for package in packages:
        package_name = package['fields']['Name']['stringValue']
        package_version = package['fields']['Version']['stringValue']
        package_id = package['fields']['ID']['stringValue']
        if package_name in name_to_version:
            name_to_version[package_name].append[(package_version, package_id)]
        else:
            name_to_version[package_name] = [(package_version, package_id)]

    # get matching packages
    matching_packages = []
    data = json.loads(event["body"])
    for query in data:
        query_name = query['Name']
        query_version = query['Version']
        
        if len(query_version) == 5: # exact version
            if query_name == "*":
                for name in name_to_version:
                    for version in name_to_version[name]:
                        if version[0] == query_version:
                            matching_packages.append((name, version[0], version[1]))
            else:
                for version in name_to_version[query_name]:
                    if version[0] == query_version:
                        matching_packages.append((query_name, version[0], version[1]))

        elif query_version[0] == '^': # carat
            query_version = query_version[1:]
            if query_name == "*":
                for name in name_to_version:
                    for version in name_to_version[name]:
                        if fitsCaratTarget(query_version, version[0]):
                            matching_packages.append((name, version[0], version[1]))
            else:
                for version in name_to_version[query_name]:
                    if fitsCaratTarget(query_version, version[0]):
                        matching_packages.append((query_name, version[0], version[1]))

        elif query_version[0] == '~': # tilde
            query_version = query_version[1:]
            if query_name == "*":
                for name in name_to_version:
                    for version in name_to_version[name]:
                        if fitsTildeTarget(query_version, version[0]):
                            matching_packages.append((name, version, name_to_version[name][1]))
            else:
                for version in name_to_version[query_name]:
                    if fitsTildeTarget(query_version, version[0]):
                        matching_packages.append((query_name, version[0], version[1]))

        else: # bounded range
            query_version_low = query_version[0:5]
            query_version_high = query_version[6:]
            if query_name == "*":
                for name in name_to_version:
                    for version in name_to_version[name]:
                        if fitsBoundedRangeTarget(query_version_low, query_version_high, version[0]):
                            matching_packages.append((name, version[0], version[1]))
            else:
                for version in name_to_version[query_name]:
                    if fitsBoundedRangeTarget(query_version_low, query_version_high, version[0]):
                        matching_packages.append((query_name, version[0], version[1]))

    # return in proper format
    matching_packages = [{"Version" : v, "Name" : n, "ID" : i} for (n, v, i) in matching_packages]
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(matching_packages)
    }
      
def fitsTildeTarget(target, version):
    return int(version[0]) == int(target[0]) and int(version[2]) == int(target[2]) and int(version[4]) >= int(target[4])

def fitsCaratTarget(target, version):

    same_minor_higher_or_equal_patch = int(version[0]) == int(target[0]) and int(version[2]) == int(target[2]) and int(version[4]) >= int(target[4])
    higher_minor = int(version[0]) == int(target[0]) and int(version[2]) > int(target[2])

    return same_minor_higher_or_equal_patch or higher_minor

def fitsBoundedRangeTarget(targetLow, targetHigh, version):
    major_in_between_targets_non_inclusive = int(version[0]) < int(targetHigh[0]) and int(version[0]) > int(targetLow[0])
    major_is_low_and_same_minor_higher_or_equal_patch = int(version[0]) == int(targetLow[0]) and int(version[2]) == int(targetLow[2]) and int(version[4]) >= int(targetLow[4])
    major_is_low_and_higher_minor = int(version[0]) == int(targetLow[0]) and int(version[2]) > int(targetLow[2])
    major_is_high_and_same_minor_lower_or_equal_patch = int(version[0]) == int(targetHigh[0]) and int(version[2]) == int(targetHigh[2]) and int(version[4]) <= int(targetHigh[4])
    major_is_high_and_lower_minor = int(version[0]) == int(targetHigh[0]) and int(version[2]) < int(targetHigh[2])
    
    return major_in_between_targets_non_inclusive or major_is_low_and_same_minor_higher_or_equal_patch or major_is_low_and_higher_minor or major_is_high_and_same_minor_lower_or_equal_patch or major_is_high_and_lower_minor
