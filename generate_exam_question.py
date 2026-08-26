import boto3

bedrockrt = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = "amazon.nova-lite-v1:0"

prompt = (
    "Generate an Exam question for the AWS Associate Developer Exam. DVA-C02, "
    "medium difficulty, three options for multiple choice, JSON formatted with "
    "question, choices, and a flag for correct or not."
)

resp = bedrockrt.converse(
    modelId=model_id,
    messages=[{"role": "user", "content": [{"text": prompt}]}],
    inferenceConfig={"temperature": 0.7, "topP": 0.9, "maxTokens": 500},
)

print(resp["output"]["message"]["content"][0]["text"])
