import json
import time
import random
import boto3

region         = "us-east-1"                   # Nova Reel is available here
model_id       = "amazon.nova-reel-v1:1"       # Current Nova Reel model ID
output_bucket  = "pgr301-couch-explorers"      # <-- your bucket
output_prefix  = "generated_videos/"           # folder in your bucket

# Important!! Change this before your investor demo :-)
prompt = "Investors with circus hats enthusiastically funding an AI startup; upbeat mood; smooth dolly-in; soft studio lighting; shallow depth of field."

fps        = 24
dimension  = "1280x720"
duration_s = 6                                 
seed       = random.randint(0, 2_147_483_646)

bedrockrt = boto3.client("bedrock-runtime", region_name=region)

model_input = {
    "taskType": "TEXT_VIDEO",
    "textToVideoParams": {
        "text": prompt
    },
    "videoGenerationConfig": {
        "durationSeconds": duration_s,
        "fps": fps,
        "dimension": dimension,
        "seed": seed,
    }
}

# Where the model should save results in your S3 bucket
output_data_config = {
    "s3OutputDataConfig": {
        "s3Uri": f"s3://{output_bucket}/{output_prefix}"
    }
}

# ===== Start async video generation =====
start = bedrockrt.start_async_invoke(
    modelId=model_id,
    modelInput=model_input,
    outputDataConfig=output_data_config
)

invocation_arn = start["invocationArn"]
print(f"Started Nova Reel job: {invocation_arn}")

# ===== Poll for completion =====
status = "InProgress"
while status == "InProgress":
    resp = bedrockrt.get_async_invoke(invocationArn=invocation_arn)
    status = resp["status"]
    print(f"Status: {status}")
    if status == "Failed":
        # When it fails, a video-generation-status.json will be written with details.
        raise RuntimeError(f"Video generation failed: {json.dumps(resp, default=str)}")
    if status == "Completed":
        break
    time.sleep(5)


invocation_id = invocation_arn.rsplit("/", 1)[-1]
base_uri = f"s3://{output_bucket}/{output_prefix}{invocation_id}/"
print(f"Done! Check your S3 folder: {base_uri}")
print(f"Full video should be at: {base_uri}output.mp4")
