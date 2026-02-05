#!/usr/bin/env bash
set -e

ENDPOINT=http://localhost:4566
ZIP=image_service.zip

echo "Creating the ZIP file"
rm -f $ZIP
cd src
zip -r ../$ZIP .
cd ..

echo "Updating the lambda code"

for fn in create-image list-images get-image delete-image; do
  aws --endpoint-url=$ENDPOINT lambda update-function-code \
    --function-name $fn \
    --zip-file fileb://$ZIP
done

echo "Deployment completed"
