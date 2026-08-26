import json
import time
import random
import boto3

# Nova Reel is legacy (winding down alongside Nova Canvas/Omni/Premier as of 2026).
# Luma Ray is the only ACTIVE text-to-video model on Bedrock, and it only lives in us-west-2.
# Async output requires a same-region S3 bucket — the class eu-west-1 buckets will NOT work here;
# create your own us-west-2 bucket and point output_bucket at it.
region         = "us-west-2"
model_id       = "luma.ray-v2:0"
output_bucket  = "glennbech-bedrock-videos-usw2"   # provisioned by infra/main.tf
output_prefix  = "generated_videos/"

# Important!! Change this before your investor demo :-)
prompt = "Investors with circus hats enthusiastically funding an AI startup; upbeat mood; smooth dolly-in; soft studio lighting; shallow depth of field."

seed = random.randint(0, 2_147_483_646)

bedrockrt = boto3.client("bedrock-runtime", region_name=region)

model_input = {
    "prompt": prompt,
    "aspect_ratio": "16:9",
    "duration": "5s",
    "resolution": "720p",
    "loop": False,
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
