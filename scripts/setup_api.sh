#!/usr/bin/env bash
set -e

ENDPOINT=http://localhost:4566
REGION=us-east-1
STAGE=dev
API_NAME=image-service-api
ROLE_ARN=arn:aws:iam::000000000000:role/lambda-role
ZIP_FILE=image_service.zip

echo "Building Lambda ZIP..."
rm -f $ZIP_FILE
cd src
zip -r ../$ZIP_FILE .
cd ..

echo "Creating Lambdas..."

create_lambda () {
  FUNCTION_NAME=$1
  HANDLER=$2

  aws --endpoint-url=$ENDPOINT lambda create-function \
    --function-name $FUNCTION_NAME \
    --runtime python3.9 \
    --role $ROLE_ARN \
    --handler $HANDLER \
    --zip-file fileb://$ZIP_FILE \
    --region $REGION \
    2>/dev/null || echo "  ↪ Lambda $FUNCTION_NAME already exists"
}

create_lambda create-image handlers.create_image.handler
create_lambda list-images handlers.list_images.handler
create_lambda get-image handlers.get_image.handler
create_lambda delete-image handlers.delete_image.handler

echo "Creating API Gateway..."

API_ID=$(aws --endpoint-url=$ENDPOINT apigateway create-rest-api \
  --name $API_NAME \
  --query id \
  --output text 2>/dev/null || \
  aws --endpoint-url=$ENDPOINT apigateway get-rest-apis \
    --query "items[?name=='$API_NAME'].id | [0]" \
    --output text)

echo "  API_ID=$API_ID"

ROOT_ID=$(aws --endpoint-url=$ENDPOINT apigateway get-resources \
  --rest-api-id $API_ID \
  --query "items[?path=='/'].id | [0]" \
  --output text)

echo "Creating /images resource..."

IMAGES_ID=$(aws --endpoint-url=$ENDPOINT apigateway create-resource \
  --rest-api-id $API_ID \
  --parent-id $ROOT_ID \
  --path-part images \
  --query id \
  --output text 2>/dev/null || \
  aws --endpoint-url=$ENDPOINT apigateway get-resources \
    --rest-api-id $API_ID \
    --query "items[?path=='/images'].id | [0]" \
    --output text)

echo "Creating /images/{image_id} resource..."

IMAGE_ID_RES=$(aws --endpoint-url=$ENDPOINT apigateway create-resource \
  --rest-api-id $API_ID \
  --parent-id $IMAGES_ID \
  --path-part "{image_id}" \
  --query id \
  --output text 2>/dev/null || \
  aws --endpoint-url=$ENDPOINT apigateway get-resources \
    --rest-api-id $API_ID \
    --query "items[?path=='/images/{image_id}'].id | [0]" \
    --output text)

add_method () {
  RESOURCE_ID=$1
  METHOD=$2
  FUNCTION=$3

  aws --endpoint-url=$ENDPOINT apigateway put-method \
    --rest-api-id $API_ID \
    --resource-id $RESOURCE_ID \
    --http-method $METHOD \
    --authorization-type NONE \
    2>/dev/null || true

  aws --endpoint-url=$ENDPOINT apigateway put-integration \
    --rest-api-id $API_ID \
    --resource-id $RESOURCE_ID \
    --http-method $METHOD \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri arn:aws:apigateway:$REGION:lambda:path/2015-03-31/functions/arn:aws:lambda:$REGION:000000000000:function:$FUNCTION/invocations
}

echo "Wiring the methods..."

add_method $IMAGES_ID POST create-image
add_method $IMAGES_ID GET list-images
add_method $IMAGE_ID_RES GET get-image
add_method $IMAGE_ID_RES DELETE delete-image

echo "Deploying API..."

aws --endpoint-url=$ENDPOINT apigateway create-deployment \
  --rest-api-id $API_ID \
  --stage-name $STAGE

echo "Script execution completed. Base URL:"
echo "http://localhost:4566/restapis/$API_ID/$STAGE/_user_request_"
