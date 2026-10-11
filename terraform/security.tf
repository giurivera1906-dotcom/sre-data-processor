
resource "aws_security_group" "lambda" {
  name        = "${var.project_name}-lambda"
  description = "Lambda egress to Redis and S3"
  vpc_id      = aws_vpc.main.id

  egress {
    description = "Redis access"
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    description     = "S3 Gateway Endpoint HTTPS"
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    prefix_list_ids = [aws_vpc_endpoint.s3.prefix_list_id]
  }
}

resource "aws_security_group" "redis" {
  name        = "${var.project_name}-redis"
  description = "Redis accepts connections from Lambda only"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Redis from Lambda"
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.lambda.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
