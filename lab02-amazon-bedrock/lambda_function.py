import json
import uuid
import boto3

def get_named_parameter(event, name):
    """
    Get a parameter from the lambda event
    """
    return next(item for item in event['parameters'] if item['name'] == name)['value']

def get_uml_diagram(yml_code):
    """
    Get a UML Diagram

    Save image to S3
    """

    return {"imageUrl":"s3://test-bucket/prefix/image.jpg"}


def get_unit_test_code(yml_code):
    """
    Generate unit test code to invoke an API
    
    """
    
    codeBody = """
    Here is the unit test code:
    ```python
    import requests
    
    url = "http://petstore.swagger.io/v2/pet"
    
    payload = { "name": "Buddy", "photoUrls": [ "http://pet-images.com/buddy.jpg" ], "category": { "id": 1, "name": "Dogs" }, "status": "available" } 
    headers = { 'Content-Type': 'application/json' }
    
    response = requests.request("POST", url, headers=headers, json=payload)
    
    print(response.text)
    ```
    """
    
    return {"codeBody": codeBody}

def lambda_handler(event, context):
    # get the action group used during the invocation of the lambda function
    actionGroup = event.get('actionGroup', '')
    
    # name of the function that should be invoked
    function = event.get('function', '')
    
    # parameters to invoke function with
    parameters = event.get('parameters', [])

    if function == 'get_uml_diagram':
        yml_code = get_named_parameter(event, "yml_body")
        if yml_code:
            response = get_uml_diagram(yml_code)
            responseBody = {'TEXT': {'body': json.dumps(response)}}
        else:
            responseBody = {'TEXT': {'body': 'Missing YML code.'}}

    elif function == 'get_unit_test_code':
        yml_code = get_named_parameter(event, "yml_body")

        if yml_code:
            response = get_unit_test_code(yml_code)
            responseBody = {'TEXT': {'body': json.dumps(response)}}
        else:
            responseBody = {'TEXT': {'body': 'Missing YML code.'}}

    else:
        responseBody = {'TEXT': {'body': 'Invalid function'}}

    action_response = {
        'actionGroup': actionGroup,
        'function': function,
        'functionResponse': {
            'responseBody': responseBody
        }
    }

    function_response = {'response': action_response, 'messageVersion': event['messageVersion']}
    print("Response: {}".format(function_response))

    return function_response
