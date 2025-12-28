# API Documentation

## Overview
Complete REST API for AIDomesticCoreAIJ platform

### Base URL
```
https://api.example.com/api/v1
```

### Authentication
All endpoints (except `/auth/*`) require Bearer token authentication.

```
Authorization: Bearer <token>
```

---

## Authentication Endpoints

### POST /auth/register
Register a new user account.

**Request:**
```json
{
  "username": "user@example.com",
  "password": "secure_password",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "user@example.com",
  "email": "user@example.com",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "created_at": "2025-12-01T10:00:00Z"
}
```

### POST /auth/login
Authenticate user and get access token.

**Request:**
```json
{
  "username": "user@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "expires_in": 3600
}
```

### POST /auth/refresh
Refresh authentication token.

**Request:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "expires_in": 3600
}
```

---

## Quantum Computing Endpoints

### GET /quantum/circuits
List all quantum circuits.

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `limit` (int): Items per page (default: 20)
- `type` (string): Circuit type filter

**Response:**
```json
{
  "data": [
    {
      "id": "circuit_001",
      "name": "Bell State",
      "qubits": 2,
      "gates": 3,
      "depth": 2,
      "created_at": "2025-12-01T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150
  }
}
```

### POST /quantum/circuits
Create a new quantum circuit.

**Request:**
```json
{
  "name": "New Circuit",
  "description": "Test quantum circuit",
  "qubits": 3,
  "gates": ["H", "CNOT", "RZ"],
  "parameters": {
    "backend": "simulator",
    "shots": 1000
  }
}
```

### POST /quantum/execute
Execute a quantum circuit.

**Request:**
```json
{
  "circuit_id": "circuit_001",
  "backend": "simulator",
  "shots": 1000
}
```

**Response:**
```json
{
  "job_id": "job_001",
  "status": "running",
  "backend": "simulator",
  "created_at": "2025-12-01T10:00:00Z"
}
```

### GET /quantum/results/{job_id}
Get execution results.

**Response:**
```json
{
  "job_id": "job_001",
  "status": "completed",
  "result_count": 1000,
  "counts": {
    "00": 245,
    "01": 12,
    "10": 18,
    "11": 725
  },
  "execution_time_ms": 1234
}
```

---

## Vision Endpoints

### POST /vision/upload
Upload image for processing.

**Request:** (multipart/form-data)
```
file: <binary_image_data>
task: "object_detection"
```

**Response:**
```json
{
  "id": "vision_001",
  "status": "processing",
  "created_at": "2025-12-01T10:00:00Z"
}
```

### GET /vision/results/{vision_id}
Get vision processing results.

**Response:**
```json
{
  "id": "vision_001",
  "status": "completed",
  "detections": [
    {
      "class": "person",
      "confidence": 0.95,
      "bbox": [10, 20, 100, 150]
    }
  ]
}
```

---

## Federated Learning Endpoints

### GET /federated/models
List federated models.

**Response:**
```json
{
  "data": [
    {
      "id": "model_001",
      "name": "Federated Model",
      "version": "1.0.0",
      "clients": 10,
      "accuracy": 0.95,
      "status": "active"
    }
  ]
}
```

### POST /federated/train
Start federated training round.

**Request:**
```json
{
  "model_id": "model_001",
  "num_rounds": 5,
  "epochs_per_round": 3,
  "batch_size": 32
}
```

**Response:**
```json
{
  "job_id": "train_job_001",
  "status": "started",
  "rounds": 5
}
```

### GET /federated/status/{job_id}
Get training status.

**Response:**
```json
{
  "job_id": "train_job_001",
  "status": "completed",
  "rounds_completed": 5,
  "final_accuracy": 0.96,
  "duration_seconds": 3600
}
```

---

## Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid request parameters",
    "details": {
      "field": "username",
      "issue": "required field missing"
    }
  }
}
```

### HTTP Status Codes
- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Rate Limited
- `500` - Internal Server Error
- `503` - Service Unavailable

---

## Rate Limiting

### Limits
- Anonymous: 100 requests/hour
- Authenticated: 1000 requests/hour
- Premium: Unlimited

### Headers
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640000000
```

---

## Pagination

All list endpoints support pagination.

### Query Parameters
- `page` (int): Page number (default: 1)
- `limit` (int): Items per page (default: 20, max: 100)
- `sort` (string): Sort field (default: created_at)
- `order` (string): Sort order (asc/desc, default: desc)

### Response Format
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 1000,
    "pages": 50
  }
}
```

---

## Webhooks

### Register Webhook
```
POST /webhooks
{
  "url": "https://example.com/webhook",
  "events": ["job.completed", "model.updated"],
  "active": true
}
```

### Webhook Events
- `job.completed` - Job execution completed
- `model.updated` - Model updated
- `error.occurred` - Error occurred
- `training.started` - Training started
- `training.completed` - Training completed

---

## SDK Availability

- **Python**: `pip install aiplatform-sdk`
- **JavaScript**: `npm install aiplatform-sdk`
- **Go**: `go get github.com/yourusername/aiplatform-go`

