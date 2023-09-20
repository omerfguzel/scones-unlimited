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