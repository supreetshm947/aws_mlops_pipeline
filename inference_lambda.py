import json
import boto3
import os

ENDPOINT_NAME = os.environ.get("ENDPOINT_NAME")
runtime = boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    print("Received event:" + json.dumps(event, indent=2))

    data = json.loads(json.dumps(event))
    payload = data["data"]
    print(payload)

    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                        ContentType='text/csv',
                                        Body=payload)
    
    print(response)

    result = response['Body'].read().decode('utf-8')
    
    return {
        'statusCode': 200,
        'body': json.dumps({'predictions': result})
    }
