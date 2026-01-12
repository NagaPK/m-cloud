### Image Service API Documentation

``
Base URL (Local) - http://localhost:4566/restapis/{API_ID}/dev/_user_request_
``

### 1. Create Image (Metadata + Upload URL) - POST /images
  Request Body:
  {
    "owner_id": "test123",
    "content_type": "image/png",
    "size_bytes": 12345,
    "tags": ["profile", "avatar"]
  }

  Response: 201
```json
  {
    "image_id": "abc123",
    "upload_url": "https://...",
    "expires_in": 900
  }
```

### 2. Upload Image (S3) 

#### PUT {upload_url}

````
  Headers: Content-Type: image/png
  Body: Binary file

  Response: 200 OK
````

#### 3. List Images
 ```` 
  GET /images
  Query Params (at least one required)
  Param	    Description
  -------------------------
  owner_id	Filter by owner
  tag       Filter by tag

  Example:
  /images?owner_id=test123
  ````

  Response 200
  ```json
  [
    {
      "image_id": "abc123",
      "tags": ["profile"],
      "created_at": "2026-01-11T12:00:00Z"
    }
  ]
  ```

#### 4. Get Image (Download URL)
  ````
  GET /images/{image_id}
````
  Response 200
  ```json
  {
    "image_id": "abc123",
    "download_url": "https://...",
    "expires_in": 900
  }
  ```

#### 5. Download Image
  ```
  GET {download_url}
  Response: Binary image
  ```

#### 6. Delete Image (Hard Delete)
  ```
  DELETE /images/{image_id}
  Response: 204 No Content
  ```
#### Error Responses:

```
Code  Description
----------------
400	  Invalid request
404	  Image not found
500	  Internal error
```

#### Usage Notes
- Upload & download URLs expire
- Metadata is created before upload
- Deletion removes metadata + S3 object
- Authentication not yet enabled
