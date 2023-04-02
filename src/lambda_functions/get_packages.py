import json
import requests

def lambda_handler(event, context):
  
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
    
def getCaratVersionNumbers(startingVersion):
  version_numbers = set()
  patch_number = int(startingVersion[-1])
  minor_number = int(startingVersion[-3])
  while minor_number < 10:
    while patch_number < 10:
      version_numbers.add(startingVersion[:-3] + str(minor_number) + '.' + str(patch_number))
      patch_number += 1
    minor_number += 1
    patch_number = 1
  return version_numbers


def getTildeVersionNumbers(startingVersion):
  version_numbers = set()
  patch_number = int(startingVersion[-1])
  while patch_number < 10:
    version_numbers.add(startingVersion[:-1] + str(patch_number))
    patch_number += 1
    
  return version_numbers
  