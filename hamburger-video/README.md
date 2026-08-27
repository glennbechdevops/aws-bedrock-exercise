# Hamburger video Lambda

This SAM application starts an asynchronous Luma Ray video job through Amazon Bedrock. Bedrock writes the completed MP4 to the configured S3 bucket, so the Lambda returns a `202` response instead of waiting for the video to finish.

The output bucket must already exist in `us-west-2`. Create one with the Terraform configuration in `infra/` if needed.

## Build and test

```shell
cd hamburger-video
sam validate
sam build --use-container
sam local invoke HamburgerVideoFunction -e events/event.json
```

The local invoke requires AWS credentials and Bedrock model access because it starts a real generation job.

## Deploy

Deploy the SAM stack in `eu-west-1` and pass the existing `us-west-2` bucket name:

```shell
sam deploy \
  --guided \
  --region eu-west-1 \
  --parameter-overrides OutputBucket=<your-us-west-2-bucket>
```

Send an optional JSON prompt to the API endpoint:

```shell
curl -X POST "$URL" \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"A crispy hamburger on a wooden table, cinematic food commercial."}'
```

The response is a `202` with an `invocationArn`. Poll the status endpoint until the job completes; the response then contains a presigned URL for the MP4:

```shell
curl "$URL/status?arn=<invocationArn>"
# {"status":"InProgress"}  ...  {"status":"Completed","key":"...","url":"https://...presigned..."}
```

The API also sends CORS headers (and answers the OPTIONS preflight), so the browser frontend in `../frontend/` can call it directly.