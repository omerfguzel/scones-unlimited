### LAMBDA 1 ###
import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # Get the s3 address from the Step Function event input
    key = event["s3_key"]  # Fill in the field name
    bucket = event["s3_bucket"]  # Fill in the field name
    
    # Download the data from S3 to /tmp/image.png
    s3.download_file(bucket, key, '/tmp/image.png')  # Fill in the correct parameters
    
    # Read the data from a file and base64 encode it
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "s3_bucket": bucket,
            "s3_key": key,
            "image_data": image_data,
            "inferences": []
        }
    }

##################################################################################
##################################################################################

### LAMBDA 2 ###

import json
import sagemaker
import base64
from sagemaker.serializers import IdentitySerializer

ENDPOINT = "image-classifier-endpoint" 

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['body']['image_data'])

    # Instantiate a Predictor
    predictor = sagemaker.predictor.Predictor(ENDPOINT)

    # For this model the IdentitySerializer needs to be "image/png"
    predictor.serializer = IdentitySerializer("image/png")

    # Make a prediction:
    inferences = predictor.predict(image)

    # We return the data back to the Step Function    
    event["body"]["inferences"] = json.loads(inferences)
    return {
        'statusCode': 200,
        'body': event['body']
    }

##################################################################################
##################################################################################

### LAMBDA 3 ###

import json

THRESHOLD = .9

def lambda_handler(event, context):
 
    inferences = event['body']['inferences']

    meets_threshold = any([x > THRESHOLD for x in inferences])

    if meets_threshold:
        pass
    else:
        raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }