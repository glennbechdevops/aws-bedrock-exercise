# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This is a **hands-on lab/exercise repo** (Sopra Steria Bedrock lab). It is intentionally a starting point, not a finished application. The three Python scripts at the repo root are deliberately simple, hardcoded, and low-quality — students are expected to fork the repo, run them to understand Bedrock, then rewrite them as AWS Lambda functions using AWS SAM. The README (in Norwegian) is the authoritative spec for the exercise.

When helping in this repo, keep that framing in mind: improvements to the scripts (env vars, parameterization, error handling) are usually part of the exercise the user is doing, not cleanup you should apply preemptively.

## Scripts

Each script is a standalone Bedrock demo. All hit `bedrock-runtime` in `us-east-1` regardless of any local AWS region config (Bedrock feature availability constraint — see README).

- `generate_image.py` — Titan Image Generator v1 (`amazon.titan-image-generator-v1`), synchronous `invoke_model`, base64-decodes result, uploads PNG to S3.
- `generate_video.py` — Nova Reel (`amazon.nova-reel-v1:1`), **asynchronous** `start_async_invoke` + polling loop, output written directly to S3 by Bedrock via `s3OutputDataConfig`.
- `generate_exam_question.py` — Titan Text Express (`amazon.titan-text-express-v1`), synchronous text generation, prints to stdout.

The two S3 bucket names hardcoded in the scripts (`sopra-steria-ai-day-25` in image script, `pgr301-couch-explorers` in video script) are shared class buckets — do not assume they are correct for a given student; parameterizing them is one of the exercise tasks.

## Running locally

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install boto3
python generate_image.py    # or generate_video.py / generate_exam_question.py
```

AWS credentials must be configured (`aws configure`) with access to Bedrock in `us-east-1` and write access to the target S3 bucket. There is no test suite, linter config, or build step — this is scripts, not a package.

## SAM / Lambda (the actual exercise)

The user's task is to convert one or more scripts into Lambda functions via SAM. Expected workflow when helping:

- `sam init` to scaffold, `sam build --use-container`, `sam deploy` (student figures out args).
- Infrastructure region must be `eu-west-1`; Bedrock calls stay in `us-east-1`.
- Lambda needs IAM permissions for `bedrock:InvokeModel` (and `bedrock:StartAsyncInvoke` / `GetAsyncInvoke` for video) plus S3 write.
- Video Lambda needs a high timeout (Nova Reel jobs take minutes; the sync script polls, but a Lambda would typically fire-and-forget the async invoke).
- Bucket name and other config should move to `Environment.Variables` in `template.yaml`, read via `os.environ.get(...)`.
