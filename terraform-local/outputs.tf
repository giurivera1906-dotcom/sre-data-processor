output "api_url" {
  value = aws_apigatewayv2_api.http.api_endpoint
}
output "bucket_name" {
  value = aws_s3_bucket.results.bucket
}
output "lambda_name" {
  value = aws_lambda_function.processor.function_name
}
