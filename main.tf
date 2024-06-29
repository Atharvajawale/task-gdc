provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-bucket"
}

resource "aws_rds_instance" "my_rds" {
  allocated_storage    = 10
  engine               = "mysql"
  instance_class       = "db.t2.micro"
  name                 = "mydatabase"
  username             = "admin"
  password             = "password"
  parameter_group_name = "default.mysql5.6"
}

resource "aws_glue_catalog_database" "my_glue_db" {
  name = "my_glue_db"
}

resource "aws_lambda_function" "my_lambda" {
  function_name = "my-function"
  image_uri     = "339712764097.dkr.ecr.us-east-1.amazonaws.com/my-repository:latest"
  role          = aws_iam_role.lambda_exec.arn
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "lambda_exec_attach" {
  name       = "lambda_exec_policy_attach"
  roles      = [aws_iam_role.lambda_exec.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
