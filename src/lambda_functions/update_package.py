import json
import requests
import datetime

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

    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/" + package_id
    document = requests.get(url).json()
    # print(document)
    
    if "error" in document or document["fields"]['name']['stringValue'] != package_name or document["fields"]['version']['stringValue'] != package_version:
        
        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "Package does not exist."
            })
        }
        
    # for reference
    # document = {
    #     "fields" : {
    #         "name" : {
    #             "stringValue" : package_name
    #         },
    #         "version" : {
    #             "stringValue" : package_version
    #         },
    #         "id" : {
    #             "stringValue" : package_id
    #         },
    #         "content" : {
    #             "stringValue" : package_content
    #         },
    #         "url" : {
    #             "stringValue" : package_url
    #         },
    #         "jsprogram" : {
    #             "stringValue" : package_jsprogram
    #         },
    #         "history" : {
    #             "arrayValue" : {
    #                 'values' : [
    #                     {
    #                         'mapValue': {
    #                             'fields': {
    #                                 'Action': {
    #                                     'stringValue': 'CREATE'
    #                                 }, 
    #                                 'User': {
    #                                     'mapValue': {
    #                                         'fields': {
    #                                             'name': {
    #                                                 'stringValue': 'UNIMPLEMENTED'
    #                                             }, 
    #                                             'isAdmin': {
    #                                                 'booleanValue': True
    #                                             }
    #                                         }
    #                                     }
    #                                 }, 
    #                                 'Date': {
    #                                     'stringValue': date
    #                                 }
    #                             }
    #                         }
    #                     }
    #                 ]
    #             }
    #         }
    #     }
    # } 

    # TODO: do we need to check that union type is maintained here?
    if package_content != 'notFound': document["fields"]['content']['stringValue'] = package_content
    if package_url != 'notFound': document["fields"]['url']['stringValue'] = package_url
    if package_jsprogram != 'notFound': document["fields"]['jsprogram']['stringValue'] = package_jsprogram

    # used https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python for utc iso date
    date = datetime.datetime.utcnow().isoformat()
    date = date[0:date.index('.')]+'Z'

    history_entry = {
        'mapValue': {
            'fields': {
                'Action': {
                    'stringValue': 'UPDATE'
                }, 
                'User': {
                    'mapValue': {
                        'fields': {
                            'name': {
                                'stringValue': 'UNIMPLEMENTED'
                            }, 
                            'isAdmin': {
                                'booleanValue': True
                            }
                        }
                    }
                }, 
                'Date': {
                    'stringValue': date
                }
            }
        }
    }

    document['fields']['history']['arrayValue']['values'].append(history_entry)

    document.pop('name') # NOT the name field; necessary to remove for posting

    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages/" + package_id
    response = requests.delete(url).json() # unchecked
        
    url = "https://firestore.googleapis.com/v1/projects/acme-register/databases/(default)/documents/packages?documentId=" + package_id
    response = requests.post(url, json.dumps(document)).json()
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "error": "Version is updated."
        })
    }