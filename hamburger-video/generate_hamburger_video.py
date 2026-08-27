import json
import os

import boto3
from botocore.exceptions import ClientError


BEDROCK_REGION = os.environ.get("BEDROCK_REGION", "us-west-2")
MODEL_ID = os.environ.get("MODEL_ID", "luma.ray-v2:0")
OUTPUT_BUCKET = os.environ.get("OUTPUT_BUCKET", "")
OUTPUT_PREFIX = os.environ.get("OUTPUT_PREFIX", "generated_hamburger_videos/")
DEFAULT_PROMPT = (
    "A delicious gourmet hamburger being assembled layer by layer, "
    "fresh lettuce, tomato, cheese, and a toasted sesame bun; "
    "appetizing food commercial; smooth camera movement; warm studio lighting."
)

bedrock_runtime = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)
# The output bucket lives in the same region as the model (us-west-2);
# the client must match it for presigned URLs to resolve correctly.
s3_client = boto3.client("s3", region_name=BEDROCK_REGION)


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body),
    }


def _request_body(event):
    body = event.get("body", event)
    if body is None:
        return {}
    if isinstance(body, str):
        return json.loads(body) if body else {}
    return body


def start_job(request):
    prompt = request.get("prompt", DEFAULT_PROMPT)
    if not isinstance(prompt, str) or not prompt.strip():
        return _response(400, {"error": "prompt must be a non-empty string"})

    model_input = {
        "prompt": prompt.strip(),
        "aspect_ratio": request.get("aspect_ratio", "16:9"),
        "duration": request.get("duration", "5s"),
        "resolution": request.get("resolution", "720p"),
        "loop": request.get("loop", False),
    }
    output_uri = f"s3://{OUTPUT_BUCKET}/{OUTPUT_PREFIX}"

    response = bedrock_runtime.start_async_invoke(
        modelId=MODEL_ID,
        modelInput=model_input,
        outputDataConfig={"s3OutputDataConfig": {"s3Uri": output_uri}},
    )
    return _response(
        202,
        {
            "status": "InProgress",
            "invocationArn": response["invocationArn"],
            "outputUri": output_uri,
        },
    )


def _find_video_key(bucket, prefix, invocation_id):
    """Bedrock writes the MP4 under a subfolder named after the invocation id."""
    candidates = [f"{prefix.rstrip('/')}/{invocation_id}", prefix]
    for candidate in candidates:
        listing = s3_client.list_objects_v2(Bucket=bucket, Prefix=candidate)
        for obj in listing.get("Contents", []):
            if obj["Key"].endswith(".mp4") and invocation_id in obj["Key"]:
                return obj["Key"]
    return None


def job_status(invocation_arn):
    job = bedrock_runtime.get_async_invoke(invocationArn=invocation_arn)
    status = job["status"]

    if status == "Failed":
        return _response(
            200, {"status": status, "failureMessage": job.get("failureMessage", "")}
        )
    if status != "Completed":
        return _response(200, {"status": status})

    s3_uri = job["outputDataConfig"]["s3OutputDataConfig"]["s3Uri"]
    bucket, _, prefix = s3_uri.replace("s3://", "", 1).partition("/")
    invocation_id = invocation_arn.split("/")[-1]

    key = _find_video_key(bucket, prefix, invocation_id)
    if key is None:
        # Bedrock says Completed but the object hasn't landed yet; poll again.
        return _response(200, {"status": "InProgress"})

    url = s3_client.generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=3600
    )
    return _response(200, {"status": "Completed", "key": key, "url": url})


def lambda_handler(event, context):
    if not OUTPUT_BUCKET:
        return _response(500, {"error": "OUTPUT_BUCKET environment variable is not configured"})

    try:
        if event.get("httpMethod") == "GET":
            arn = (event.get("queryStringParameters") or {}).get("arn", "")
            if not arn:
                return _response(400, {"error": "missing 'arn' query parameter"})
            return job_status(arn)
        return start_job(_request_body(event))
    except ClientError as err:
        return _response(502, {"error": err.response["Error"].get("Message", str(err))})
    except (ValueError, json.JSONDecodeError) as err:
        return _response(400, {"error": str(err)})
