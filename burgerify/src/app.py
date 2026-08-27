"""
Burgerify — drop a burger monster into any photo.

Pipeline (Stability Core has no image-to-image mode, so we cheat):
  1. Nova Lite (multimodal, us-east-1) describes the subject in the photo.
  2. Stability Core (us-west-2) generates a scene with a colossal burger
     monster looming next to that subject.
  3. Result is written to S3, and a presigned URL is returned.

Invoke via API Gateway:
  POST /burgerify
  {"image": "<base64 of a jpeg/png>", "context": "rampaging through a city"}
  `context` is optional extra direction for the image prompt.
"""

import base64
import json
import os
import random

import boto3

TEXT_MODEL_ID = os.environ.get("TEXT_MODEL_ID", "amazon.nova-lite-v1:0")
IMAGE_MODEL_ID = os.environ.get("IMAGE_MODEL_ID", "stability.stable-image-core-v1:1")
TEXT_REGION = os.environ.get("TEXT_REGION", "us-east-1")
IMAGE_REGION = os.environ.get("IMAGE_REGION", "us-west-2")
BUCKET_NAME = os.environ.get("BUCKET_NAME", "")

# Clients are created outside the handler so they are reused across warm invokes.
text_client = boto3.client("bedrock-runtime", region_name=TEXT_REGION)
image_client = boto3.client("bedrock-runtime", region_name=IMAGE_REGION)
s3_client = boto3.client("s3")


def _detect_format(image_bytes: bytes) -> str:
    """Nova's converse API wants to know the format; sniff the magic bytes."""
    if image_bytes[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if image_bytes[:3] == b"\xff\xd8\xff":
        return "jpeg"
    if image_bytes[:4] == b"RIFF" and image_bytes[8:12] == b"WEBP":
        return "webp"
    if image_bytes[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    raise ValueError("Unsupported image format (need jpeg, png, webp or gif)")


def describe_subject(image_bytes: bytes) -> str:
    """Step 1: ask Nova Lite what the person/subject in the photo looks like."""
    response = text_client.converse(
        modelId=TEXT_MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "image": {
                            "format": _detect_format(image_bytes),
                            "source": {"bytes": image_bytes},
                        }
                    },
                    {
                        "text": (
                            "Describe the main subject of this photo in 2-3 short "
                            "sentences for a caricature artist: hair, glasses, "
                            "facial hair, expression, clothing and colors, and any "
                            "distinctive accessories. Do not guess who the person "
                            "is and do not use names."
                        )
                    },
                ],
            }
        ],
        inferenceConfig={"temperature": 0.3, "maxTokens": 200},
    )
    return response["output"]["message"]["content"][0]["text"].strip()


def build_monster_prompt(description: str, extra_context: str) -> str:
    """Step 2: put a burger monster into a scene with the person from the photo."""
    prompt = (
        "A colossal friendly burger monster looming in the scene: sesame-seed bun "
        "head, googly cartoon eyes, lettuce frills, dripping melted cheese and a "
        "thick beef patty body. Beside it stands a person described as: "
        f"{description} "
        "Cinematic wide shot, vivid saturated colors, dramatic rim lighting, "
        "highly detailed illustration."
    )
    if extra_context:
        prompt += f" Additional direction: {extra_context}"
    return prompt


def generate_poster(prompt: str, seed: int) -> bytes:
    """Step 3: Stability Core, text-to-image (same call style as generate_image.py)."""
    native_request = {
        "prompt": prompt,
        "mode": "text-to-image",
        "aspect_ratio": "1:1",
        "output_format": "png",
        "seed": seed,
    }
    response = image_client.invoke_model(
        modelId=IMAGE_MODEL_ID, body=json.dumps(native_request)
    )
    model_response = json.loads(response["body"].read())
    return base64.b64decode(model_response["images"][0])


def _response(status: int, body: dict) -> dict:
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  # handy for the frontend bonus task
        },
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    # Works both behind API Gateway (event["body"]) and via direct invoke.
    raw_body = event.get("body") if isinstance(event, dict) else None
    if raw_body is not None:
        if event.get("isBase64Encoded"):
            raw_body = base64.b64decode(raw_body)
        payload = json.loads(raw_body)
    else:
        payload = event or {}

    image_b64 = payload.get("image")
    if not image_b64:
        return _response(400, {"error": "Missing 'image' (base64) in request body"})
    if not BUCKET_NAME:
        return _response(500, {"error": "BUCKET_NAME environment variable not set"})

    # `context` is the optional extra direction from the frontend.
    # `word` is the legacy field name and is still accepted.
    extra_context = str(payload.get("context") or payload.get("word") or "")[:200].strip()

    try:
        image_bytes = base64.b64decode(image_b64)
        description = describe_subject(image_bytes)
    except ValueError as err:
        return _response(400, {"error": str(err)})

    prompt = build_monster_prompt(description, extra_context)
    seed = random.randint(0, 2147483647)
    poster_bytes = generate_poster(prompt, seed)

    s3_key = f"burgerify/burger_{seed}.png"
    s3_client.put_object(
        Bucket=BUCKET_NAME, Key=s3_key, Body=poster_bytes, ContentType="image/png"
    )
    presigned_url = s3_client.generate_presigned_url(
        "get_object", Params={"Bucket": BUCKET_NAME, "Key": s3_key}, ExpiresIn=3600
    )

    return _response(
        200,
        {
            "bucket": BUCKET_NAME,
            "key": s3_key,
            "url": presigned_url,
            "subject_description": description,
            "prompt": prompt,
            "seed": seed,
        },
    )
