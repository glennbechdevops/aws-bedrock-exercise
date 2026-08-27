#!/usr/bin/env bash
#
# Deploy the Burgerify frontend to an S3 static-website bucket in eu-west-1.
#
# Usage (from a Codespace with `aws configure` done):
#   bash frontend/deploy.sh                # bucket name derived from your GitHub user
#   bash frontend/deploy.sh my-bucket-name # explicit bucket name
#
set -euo pipefail

REGION=eu-west-1
SUFFIX="${GITHUB_USER:-$(hostname | tr -cd 'a-z0-9' | cut -c1-12)}"
BUCKET="${1:-burgerify-frontend-$(echo "$SUFFIX" | tr '[:upper:]' '[:lower:]')}"
DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Bucket: $BUCKET ($REGION)"

# Create the bucket if it doesn't exist yet (eu-west-1 needs LocationConstraint).
if ! aws s3api head-bucket --bucket "$BUCKET" 2>/dev/null; then
  aws s3api create-bucket \
    --bucket "$BUCKET" \
    --region "$REGION" \
    --create-bucket-configuration "LocationConstraint=$REGION"
  echo "Created bucket."
fi

# New buckets block public access by default; a public website bucket needs it off.
aws s3api put-public-access-block --bucket "$BUCKET" \
  --public-access-block-configuration \
  "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"

aws s3api put-bucket-policy --bucket "$BUCKET" --policy "{
  \"Version\": \"2012-10-17\",
  \"Statement\": [{
    \"Sid\": \"PublicReadForWebsite\",
    \"Effect\": \"Allow\",
    \"Principal\": \"*\",
    \"Action\": \"s3:GetObject\",
    \"Resource\": \"arn:aws:s3:::$BUCKET/*\"
  }]
}"

aws s3 website "s3://$BUCKET/" --index-document index.html

aws s3 sync "$DIR" "s3://$BUCKET/" --exclude "deploy.sh" --cache-control "no-cache"

echo
echo "Frontend live at:"
echo "  http://$BUCKET.s3-website-$REGION.amazonaws.com"
