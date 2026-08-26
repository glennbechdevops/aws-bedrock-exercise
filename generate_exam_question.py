import os
import random
import re

import boto3

bedrockrt = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = "amazon.nova-lite-v1:0"

guide_path = os.path.join(os.path.dirname(__file__), "examguide.md")
with open(guide_path, "r", encoding="utf-8") as f:
    guide = f.read()

skills = re.findall(r"^- (\d+\.\d+\.\d+ .+)$", guide, flags=re.MULTILINE)


def generate_question():
    focus_skill = random.choice(skills)

    # The real DVA-C02 exam mixes two formats. Pick one at random.
    if random.random() < 0.7:
        qtype = "multiple choice"
        num_choices = 4
        num_correct = 1
        correct_spec = "a single letter (e.g. \"B\")"
    else:
        qtype = "multiple response"
        num_choices = random.choice([5, 6])
        num_correct = random.choice([2, 3])
        correct_spec = f"an array of {num_correct} letters (e.g. [\"A\", \"C\"])"

    letters = "".join(chr(ord("A") + i) for i in range(num_choices))

    prompt = (
        "You are writing a practice question for the AWS Certified Developer - Associate "
        "(DVA-C02) exam. Use the compressed exam guide below as authoritative scope.\n\n"
        f"Focus this question on skill: **{focus_skill}**\n\n"
        f"Write ONE {qtype} question with exactly {num_choices} choices ({', '.join(letters)}), "
        f"of which exactly {num_correct} is/are correct. "
        f"Return ONLY a JSON object with keys: question, choices (object keyed {letters}), "
        f"correct ({correct_spec}), explanation (one sentence). No markdown fences.\n\n"
        "---- EXAM GUIDE ----\n"
        f"{guide}"
    )

    resp = bedrockrt.converse(
        modelId=model_id,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"temperature": 0.9, "topP": 0.9, "maxTokens": 700},
    )
    return focus_skill, qtype, resp["output"]["message"]["content"][0]["text"]


n = random.randint(1, 5)
print(f"Generating {n} random question(s)\n")

for i in range(1, n + 1):
    focus, qtype, text = generate_question()
    print(f"=== Question {i}/{n}  [{qtype}]  focus: {focus} ===")
    print(text)
    print()
