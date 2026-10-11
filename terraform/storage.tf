
resource "aws_s3_bucket" "results" {
  bucket_prefix = "${var.project_name}-results-"
  force_destroy = false
}

resource "aws_s3_bucket_versioning" "results" {
  bucket = aws_s3_bucket.results.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "results" {
  bucket                  = aws_s3_bucket.results.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "results" {
  bucket = aws_s3_bucket.results.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "AllowLambdaRoleOnly"
      Effect    = "Allow"
      Principal = { AWS = aws_iam_role.lambda.arn }
      Action    = ["s3:PutObject"]
      Resource  = "${aws_s3_bucket.results.arn}/results/*"
    }]
  })

  depends_on = [
    aws_s3_bucket_public_access_block.results
  ]
}
