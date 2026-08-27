"""Test the handler locally without SAM: python run_local.py path/to/selfie.jpg [WORD]

Needs the same setup as the other lab scripts: .venv with boto3, `aws configure` done,
and BUCKET_NAME exported (defaults below match the lab).
"""
import base64
import json
import os
import sys

os.environ.setdefault("BUCKET_NAME", "sopra-steria-ai-day-26")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from app import lambda_handler  # noqa: E402

if len(sys.argv) < 2:
    sys.exit("usage: python run_local.py <image file> [WORD]")

with open(sys.argv[1], "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

event = {"image": image_b64}
if len(sys.argv) > 2:
    event["context"] = sys.argv[2]

result = lambda_handler(event, None)
body = json.loads(result["body"])
print(json.dumps(body, indent=2))
if "url" in body:
    print("\nOpen this in a browser:\n" + body["url"])
