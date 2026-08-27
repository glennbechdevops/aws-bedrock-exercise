# Burgerify 🍔

POST a photo → get a heroic two-tone campaign poster of a burger with *your* features and "BURGER" in block letters at the bottom.

## How it works

Stability Core (`stability.stable-image-core-v1:1`) is text-to-image only, so the Lambda chains two Bedrock calls:

1. **Nova Lite** (us-east-1, multimodal) describes the subject in the photo — hair, glasses, beard, expression, clothing.
2. **Stability Core** (us-west-2) renders a stencil-style poster of a burger with those traits.
3. The PNG lands in S3 and the response contains a presigned URL.

Stack lives in `eu-west-1`, Bedrock calls cross regions — same pattern as the rest of the lab.

## Try it locally first

From the repo root (with your `.venv` active and `aws configure` done):

```bash
pip install boto3
python run_local.py selfie.jpg          # or: python run_local.py selfie.jpg KEBAB
```

Prints the JSON response including a presigned URL you can open in a browser.

## Deploy with SAM

```bash
sam build --use-container
sam deploy --guided --region eu-west-1   # accept defaults; note the BurgerifyApiUrl output
```

`--guided` asks for a stack name and saves your answers to `samconfig.toml`, so subsequent deploys are just `sam deploy`.

## Call the API

```bash
URL=<BurgerifyApiUrl from the stack outputs>

curl -s -X POST "$URL" \
  -H 'Content-Type: application/json' \
  -d "{\"image\": \"$(base64 -w0 selfie.jpg)\", \"word\": \"BURGER\"}" | jq .
```

Response:

```json
{
  "bucket": "sopra-steria-ai-day-26",
  "key": "burgerify/burger_1234567.png",
  "url": "https://...presigned...",
  "subject_description": "...",
  "prompt": "...",
  "seed": 1234567
}
```

## Frontend (bonus task 1)

`frontend/index.html` is a self-contained page: pick a photo, it resizes it in the browser, POSTs to the API and shows the poster. The API URL is entered on the page itself (and remembered in localStorage), so the frontend deploys independently of the backend stack.

Host it in an S3 static-website bucket (from a Codespace with `aws configure` done):

```bash
bash frontend/deploy.sh            # creates burgerify-frontend-<your-github-user>
bash frontend/deploy.sh my-bucket  # or pick a name yourself
```

The script creates the bucket in `eu-west-1`, turns off the public-access block, attaches a public-read bucket policy, enables website hosting and syncs the files. It prints the site URL at the end (`http://<bucket>.s3-website-eu-west-1.amazonaws.com`).

**CORS**: the browser preflights the JSON POST with an OPTIONS request, so the API must answer it — `template.yaml` now has a `Globals: Api: Cors` block for that. If the backend was deployed before that block was added, run `sam deploy` again.

## Gotchas

- **Payload limits**: API Gateway caps requests at 10 MB and Lambda at 6 MB, and base64 adds ~33% — resize big phone photos first (`convert selfie.jpg -resize 1024x1024 small.jpg`).
- **Timeout**: set to 60 s in `template.yaml`; two sequential Bedrock calls usually finish in 15–25 s.
- **IAM**: the template grants `bedrock:InvokeModel` on exactly the two model ARNs plus `s3:PutObject`/`GetObject` on the bucket. If you switch Nova Lite to the `us.amazon.nova-lite-v1:0` inference profile, add its ARN too.
- **Bonus tasks**: the handler already sends `Access-Control-Allow-Origin: *`, so the frontend bonus task (task 1 in the lab README) works against it directly — and logging `prompt`/`seed`/`key` into DynamoDB slots straight into bonus task 3.
