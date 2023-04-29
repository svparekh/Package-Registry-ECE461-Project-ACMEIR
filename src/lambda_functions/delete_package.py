import json
import requests

def lambda_handler(event, context):
    
  path_id = event['path'][9:]
  
  url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/" + path_id
  
  response = requests.get(url).json() 

  delete_response = requests.delete(url).json()

  if not("error" in response):

    # https://cloud.google.com/storage/docs/json_api/v1/objects/delete
    url = "https://storage.googleapis.com/storage/v1/b/acme-register-contents/o/"+path_id
    response = requests.delete(url)
    
    return {
      "statusCode": 200,
      "headers": {
          "Content-Type": "application/json"
      },
      "body": json.dumps({
          "error": "Package is deleted."
      })
    }
      
  return {
      "statusCode": 404,
      "headers": {
          "Content-Type": "application/json"
      },
      "body": json.dumps({
          "error": "Package does not exist."
      })
  }