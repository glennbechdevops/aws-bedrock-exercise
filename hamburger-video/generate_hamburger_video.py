import json
import os

import boto3


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


def _request_body(event):
    body = event.get("body", event)
    if body is None:
        return {}
    if isinstance(body, str):
        return json.loads(body) if body else {}
    return body


def lambda_handler(event, context):
    if not OUTPUT_BUCKET:
        raise RuntimeError("OUTPUT_BUCKET environment variable is not configured")

    request = _request_body(event)
    prompt = request.get("prompt", DEFAULT_PROMPT)
    if not isinstance(prompt, str) or not prompt.strip():
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "prompt must be a non-empty string"}),
        }

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
    invocation_arn = response["invocationArn"]

    return {
        "statusCode": 202,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "status": "InProgress",
                "invocationArn": invocation_arn,
                "outputUri": output_uri,
            }
        ),
    }