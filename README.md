## Image Service (LocalStack + AWS Serverless)

A serverless **Image Upload & Management Service** built using **AWS-style architecture** and runnable entirely **locally using LocalStack**.

The service supports:
- Uploading images with metadata
- Listing images with and without filters
- Generating secure download URLs
- Deleting images (hard delete)

The project is written in **Python 3.9+**, uses **AWS Lambda, API Gateway, S3, DynamoDB**, and follows **production-grade best practices** for structure, testing, and automation.

### Architecture Overview

```
Client (Postman)
   │
   ▼
API Gateway (LocalStack)
   │
   ▼
Lambda Functions (Python)
   │
   ├── DynamoDB (Image metadata)
   └── S3 (Image storage)
```

All AWS services are created locally using **LocalStack CE**.

---

### Project Structure

```
project-root/
├── src/
│   ├── handlers/          # Lambda handlers (entry points)
│   ├── services/          # Business logic
│   ├── repositories/      # DynamoDB access layer
│   ├── models/            # Domain models
│   ├── config.py          # Configuration
│   └── __init__.py
├── tests/                 # Unit tests (pytest)
├── scripts/
│   └── setup_api.sh       # One-click LocalStack setup
├── docker-compose.yml     # LocalStack container
├── pytest.ini             # Pytest configuration
└── README.md
```
---

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- AWS CLI v2
- zip utility

---

### Local Setup

### 1. Clone the Repository

```bash
git clone <repo-url>
cd <project-folder>
```
---

### 2️. Configure AWS CLI (Dummy Credentials)

LocalStack does not require real AWS credentials. So, we can use any dummy values.

```bash
aws configure

AWS Access Key ID: test
AWS Secret Access Key: test
Default region name: us-east-1
Default output format: json
```
---

### 3️. Start LocalStack

```bash
docker-compose up -d
```

Verify:
```bash
docker ps
```

---

### 4️. Install Python Dependencies

```bash
pip install -r requirements-dev.txt
```

---

### 5️. Create All AWS Resources

```bash
./infra/deploy_stack.sh

./scripts/setup_api.sh
```

These scripts automatically:
- Builds Lambda ZIP
- Creates Lambda functions
- Creates API Gateway
- Creates resources & methods
- Wires Lambda integrations
- Deploys the API

```bash
./scripts/re-deploy.sh
```
This will redeploy the code to the available lambdas

---

### API Usage

### Base URL

```
http://localhost:4566/restapis/{API_ID}/dev/_user_request_
```

The `API_ID` is printed at the end of `setup_api.sh` when you execute it.

---

### 1️. Create Image (Metadata + Upload URL)

**POST** `/images`

```json
{
  "owner_id": "test123",
  "content_type": "image/png",
  "size_bytes": 12345,
  "tags": ["profile", "avatar"]
}
```

**Response (201)**

```json
{
  "image_id": "abc123",
  "upload_url": "http://...",
  "expires_in": 900
}
```

---

### 2️. Upload Image (Direct to S3)

**PUT** `{upload_url}`

Headers:
```
Content-Type: image/png
```

Body:
- Binary file

---

### 3️. List Images

1) **GET** `/images`
- This will list all available images.

2) **GET** `/images`

Query params (at least one required):
- `owner_id`
- `tag`

Example:
```
/images?owner_id=test123
```
---

### 4️. Get Image (Download URL)

**GET** `/images/{image_id}`

Response:

```json
{
  "image_id": "abc123",
  "download_url": "http://...",
  "expires_in": 900
}
```
---

### 5️. Download Image

**GET** `{download_url}`

Returns binary image data.

---

### 6️. Delete Image (Hard Delete)

**DELETE** `/images/{image_id}`

Response:
```
204 No Content
```

---

## Running Unit Tests

Tests are written using pytest, and they mock all AWS dependencies.
```bash
pytest -v
```

With coverage:
```bash
pytest --cov=src
```
---

## Design Notes
- LocalStack state is ephemeral by default.
- Restarting Docker requires rerunning `setup_api.sh`
- Infrastructure is script-driven, not manual.
- Imports are Lambda-compatible.
- Authentication is skipped for now.

## Future Improvements
- OpenAPI / Swagger specification
- Pagination for list APIs
- Integration tests with LocalStack

---

## Summary
This project demonstrates a serverless backend achieving the following tasks:
1. Create APIs for:
   1. Uploading image with metadata
   2. List all images, and supports at least two filters to search
   3. View/download image
   4. Delete an image
2. Write unit tests to cover all scenarios
3. API documentation and usage instructions