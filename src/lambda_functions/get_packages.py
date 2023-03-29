import json
import requests

def lambda_handler(event, context):
  
  url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/existing-versions-by-name/"
  response = requests.get(url).json()
  documents = response['documents']
  
  name_to_version = [] # {name1: [version1, version2]}
  for document in documents:
    name = document["name"][79:]
    name_to_version[name] = []
    
    versions = document["fields"]["versions"]["arrayValue"]["values"] # [{'stringValue': '1.2.3'}, {'stringValue': '1.2.9'}]
    for version in versions:
      name_to_version[name].append(version['stringValue'])

  queries = [] # filling in an array of queries - each query is in format of tuple (name, version)
  for query in event:
    queries.append((query['Name'], query["Version"]))

  packages_that_fit_query = []
  for query in queries:
    if query[0] == "*":
      if query[1][0] == '~':
        characters_the_version_must_have = query[1][1:-1]
        for name in name_to_version:
          if name
      elif query[1][0] == '^':
        
      elif len(query[1]) == 5: # straight version
      
      else: # range of versions
        
    else:
        