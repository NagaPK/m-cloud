#!/usr/bin/env bash
set -e

ENDPOINT=http://localhost:4566
STACK_NAME=image-service-stack
REGION=us-east-1
ZIP_FILE=image_service.zip

echo "Building Lambda ZIP"
rm -f $ZIP_FILE
cd src
zip -r ../$ZIP_FILE .
cd ..

echo "Uploading the Lambda ZIP to LocalStack S3"

aws --endpoint-url=$ENDPOINT s3 mb s3://local-bucket || true
aws --endpoint-url=$ENDPOINT s3 cp $ZIP_FILE s3://local-bucket/$ZIP_FILE

echo "Deploying the CloudFormation stack"

aws --endpoint-url=$ENDPOINT cloudformation deploy \
  --stack-name $STACK_NAME \
  --template-file infra/template.yaml \
  --region $REGION \
  --capabilities CAPABILITY_NAMED_IAM

echo "Stack deployment completed"
