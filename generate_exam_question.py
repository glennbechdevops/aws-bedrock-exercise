import os
import random
import re

import boto3

bedrockrt = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = "amazon.nova-lite-v1:0"

guide_path = os.path.join(os.path.dirname(__file__), "examguide.md")
with open(guide_path, "r", encoding="utf-8") as f:
    guide = f.read()

# Pick a random specific skill line (e.g. "1.2.3 Handle the event lifecycle...")
# to bias each question toward a different corner of the syllabus.
skills = re.findall(r"^- (\d+\.\d+\.\d+ .+)$", guide, flags=re.MULTILINE)
focus_skill = random.choice(skills)

prompt = (
    "You are writing a practice question for the AWS Certified Developer - Associate "
    "(DVA-C02) exam. Use the compressed exam guide below as authoritative scope.\n\n"
    f"Focus this question on skill: **{focus_skill}**\n\n"
    "Write ONE multiple-choice question with exactly four choices (A, B, C, D), one correct. "
    "Return ONLY a JSON object with keys: question, choices (object A/B/C/D), correct (letter), "
    "explanation (one sentence why the correct answer is right). No markdown fences.\n\n"
    "---- EXAM GUIDE ----\n"
    f"{guide}"
)

resp = bedrockrt.converse(
    modelId=model_id,
    messages=[{"role": "user", "content": [{"text": prompt}]}],
    inferenceConfig={"temperature": 0.9, "topP": 0.9, "maxTokens": 700},
)

print(f"[focus: {focus_skill}]\n")
print(resp["output"]["message"]["content"][0]["text"])
