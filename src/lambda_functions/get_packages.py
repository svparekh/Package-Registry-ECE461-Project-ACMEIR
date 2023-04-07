import json
import requests

def lambda_handler(event, context):
  
  # if you can see this, CI/CD works 3

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
      
  # get target package name(s) and version(s)
  target_package_versions = {} # {name1: (1.2.3, 1.2.4, 1.2.5), name2: (1.2.3, 1.2.4, 1.2.5)}
  for query in event:
    query_name = query['Name']
    query_version = query['Version']
    
    if query_name not in target_package_versions:
      target_package_versions[query_name] = set()
    
    if len(query_version) == 5: # exact version
      target_package_versions[query_name].add(query_version)
    elif query_version[0] == '^': # carat
      target_package_versions[query_name].update(getCaratVersionNumbers(query_version))
    elif query_version[0] == '~': # tilde
      target_package_versions[query_name].update(getTildeVersionNumbers(query_version))
    else: # bounded range
    
def fitsTildeTarget(target, version):
  return version[0] == target[0] and version[2] == target[2] and version[4] >= target[4]

def fitsCaratTarget(target, version):

  same_minor_higher_or_equal_patch = version[0] == target[0] and version[2] == target[2] and version[4] >= target[4]
  higher_minor = version[0] == target[0] and version[2] > target[2]

  return same_minor_higher_or_equal_patch or higher_minor

def fitsBoundedRangeTarget(targetLow, targetHigh, version):
  major_in_between_targets_non_inclusive = version[0] < targetHigh[0] and version[0] > targetLow[0]
  major_is_low_and_same_minor_higher_or_equal_patch = version[0] == targetLow[0] and version[2] == targetLow[2] and version[4] >= targetLow[4]
  major_is_low_and_higher_minor = version[0] == targetLow[0] and version[2] > targetLow[2]
  major_is_high_and_same_minor_lower_or_equal_patch = version[0] == targetHigh[0] and version[2] == targetHigh[2] and version[4] <= targetHigh[4]
  major_is_high_and_lower_minor = version[0] == targetHigh[0] and version[2] < targetHigh[2]
  
  return major_in_between_targets_non_inclusive or major_is_low_and_same_minor_higher_or_equal_patch or major_is_low_and_higher_minor or major_is_high_and_same_minor_lower_or_equal_patch or major_is_high_and_lower_minor
