terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

variable "video_bucket_name" {
  type        = string
  description = "S3 bucket for Bedrock (Luma Ray) async video output. Must be in us-west-2."
}

resource "aws_s3_bucket" "video_output" {
  bucket = var.video_bucket_name
}

resource "aws_s3_bucket_public_access_block" "video_output" {
  bucket                  = aws_s3_bucket.video_output.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "video_bucket_name" {
  value = aws_s3_bucket.video_output.bucket
}
