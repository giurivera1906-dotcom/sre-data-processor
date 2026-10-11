variable "aws_region" {
  description = "Región AWS objetivo"
  type        = string
  default     = "us-east-1"
}
variable "project_name" {
  type    = string
  default = "sre-data-processor"
}
variable "environment" {
  type    = string
  default = "test"
}
variable "vpc_cidr" {
  type    = string
  default = "10.20.0.0/16"
}
variable "lambda_zip_path" {
  description = "Ruta de salida del ZIP de Lambda"
  type        = string
  default     = "../lambda/build/lambda.zip"
}
variable "redis_node_type" {
  type    = string
  default = "cache.t3.micro"
}
variable "api_throttle_rate" {
  type    = number
  default = 5
}
variable "api_throttle_burst" {
  type    = number
  default = 10
}
