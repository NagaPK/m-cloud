import json

def handler(event, context):
    return {
        "statusCode" : 200,
        "headers" : {
            "Content-type" : "application/json"
        },
        "body" : json.dumps({
            "status": "ok",
            "service": "image-service",
            "message": "LocalStack API Gateway + Lambda is working"
        })
    }