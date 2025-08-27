import boto3, json

bedrockrt = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = "amazon.titan-text-express-v1"

body = {
    "inputText": "Generate an Exam question for the AWS Associate Developer Exam. DVA-c02, medium difficuly, three options for multiple choice, json formated question, choices, and a flag or correct or not ",
    "textGenerationConfig": {"temperature": 0.7, "topP": 0.9, "maxTokenCount": 500}
}

resp = bedrockrt.invoke_model(
    modelId=model_id,                 # <-- key change
    contentType="application/json",
    accept="application/json",
    body=json.dumps(body)
)

print(resp["body"].read().decode("utf-8"))