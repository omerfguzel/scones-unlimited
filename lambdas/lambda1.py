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