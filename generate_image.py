import base64
import boto3
import json
import random

# Set up the AWS clients
# Stability image models live in us-west-2; Amazon's own image models (Titan, Nova Canvas)
# are retired / legacy as of 2026.
bedrock_client = boto3.client("bedrock-runtime", region_name="us-west-2")
s3_client = boto3.client("s3")

# Define the model ID and S3 bucket name (replace with your actual bucket name)
model_id = "stability.stable-image-core-v1:1"
bucket_name = "sopra-steria-ai-day-25"

# Important!!; Change this prompt to something else before the presentation with the investors!
prompt = "Investors, with circus hats, giving money to  AI startup developers with large smiles on their faces "

seed = random.randint(0, 2147483647)
s3_image_path = f"generated_images/stability_{seed}.png"

native_request = {
    "prompt": prompt,
    "mode": "text-to-image",
    "aspect_ratio": "1:1",
    "output_format": "png",
    "seed": seed,
}

response = bedrock_client.invoke_model(modelId=model_id, body=json.dumps(native_request))
model_response = json.loads(response["body"].read())

# Extract and decode the Base64 image data
base64_image_data = model_response["images"][0]
image_data = base64.b64decode(base64_image_data)

# Upload the decoded image data to S3
s3_client.put_object(Bucket=bucket_name, Key=s3_image_path, Body=image_data)