import json
import requests
import datetime
import random

def lambda_handler(event, context):

  date = datetime.datetime.utcnow().isoformat() # used https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python for utc iso date
  id = date + '-' + str(int(random.random()*1000000))
  url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/logging?documentId=" + id
  response = requests.post(url, data=json.dumps({"fields": {"event": {"stringValue" : json.dumps(event)}}})).json()

  # Needs to be tested extensively. I've tested a decent amount, but there's like 100 possible test cases. I
  # might make a generate test case  script 
  
  # get packages
  url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/"
  response = requests.get(url).json()
  packages = response['documents']
  
  # establish name->version dictionary
  name_to_version = {} # {name1: [version1, version2]}
  for package in packages:
    package_name = package['fields']['name']['stringValue']
    package_version = package['fields']['version']['stringValue']
    if package_name in name_to_version:
      name_to_version[package_name].append[package_version]
    else:
      name_to_version[package_name] = [package_version]

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
            if version == query_version:
              matching_packages.append((name, version))
      else:
          for version in name_to_version[query_name]:
            if version == query_version:
              matching_packages.append((query_name, version))

    elif query_version[0] == '^': # carat
      query_version = query_version[1:]
      if query_name == "*":
        for name in name_to_version:
          for version in name_to_version[name]:
            if fitsCaratTarget(query_version, version):
              matching_packages.append((name, version))
      else:
          for version in name_to_version[query_name]:
            if fitsCaratTarget(query_version, version):
              matching_packages.append((query_name, version))

    elif query_version[0] == '~': # tilde
      query_version = query_version[1:]
      if query_name == "*":
        for name in name_to_version:
          for version in name_to_version[name]:
            if fitsTildeTarget(query_version, version):
              matching_packages.append((name, version))
      else:
          for version in name_to_version[query_name]:
            if fitsTildeTarget(query_version, version):
              matching_packages.append((query_name, version))

    else: # bounded range
      query_version_low = query_version[0:5]
      query_version_high = query_version[6:]
      if query_name == "*":
        for name in name_to_version:
          for version in name_to_version[name]:
            if fitsBoundedRangeTarget(query_version_low, query_version_high, version):
              matching_packages.append((name, version))
      else:
          for version in name_to_version[query_name]:
            if fitsBoundedRangeTarget(query_version_low, query_version_high, version):
              matching_packages.append((query_name, version))

  # return in proper format
  matching_packages = [{"Version" : v, "Name" : n} for (n, v) in matching_packages]
  
  return {
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": json.dumps(matching_packages)
  }
    
  return json.dumps(matching_packages)

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
