# API Documentation

The Wheelchair Bot API is built with FastAPI and provides RESTful endpoints for controlling the wheelchair bot.

## Base URL

```
http://localhost:8000
```

## Interactive Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### GET /

Get API information.

**Response:**
```json
{
  "name": "Wheelchair Bot API",
  "version": "0.1.0",
  "status": "running"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

### GET /api/status

Get the current status of the wheelchair bot.

**Response:**
```json
{
  "battery_level": 85,
  "is_moving": false,
  "speed": 0,
  "direction": null
}
```

**Fields:**
- `battery_level` (integer): Battery percentage (0-100)
- `is_moving` (boolean): Whether the bot is currently moving
- `speed` (integer): Current speed percentage (0-100)
- `direction` (string|null): Current movement direction or null if stopped

### POST /api/move

Send a movement command to the wheelchair bot.

**Query Parameters:**
- `direction` (string, required): Direction to move
  - Valid values: `forward`, `backward`, `left`, `right`, `stop`
- `speed` (integer, optional): Speed percentage (0-100)
  - Default: 50

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/move?direction=forward&speed=50"
```

**Success Response:**
```json
{
  "status": "success",
  "command": "forward",
  "speed": 50
}
```

**Error Response (Invalid Direction):**
```json
{
  "error": "Invalid direction"
}
```

**Error Response (Invalid Speed):**
```json
{
  "error": "Speed must be between 0 and 100"
}
```

## Response Codes

- `200 OK`: Successful request
- `422 Unprocessable Entity`: Invalid request parameters
- `500 Internal Server Error`: Server error

## CORS

CORS is enabled for all origins in development. Configure appropriately for production.

## Rate Limiting

Currently no rate limiting is implemented. Consider adding in production.

## Authentication

Currently no authentication is implemented. Add authentication for production use.

## Examples

### Python

```python
import requests

# Get status
response = requests.get("http://localhost:8000/api/status")
status = response.json()
print(f"Battery: {status['battery_level']}%")

# Move forward
response = requests.post(
    "http://localhost:8000/api/move",
    params={"direction": "forward", "speed": 50}
)
result = response.json()
print(result)
```

### JavaScript

```javascript
// Get status
fetch('http://localhost:8000/api/status')
  .then(response => response.json())
  .then(data => console.log('Battery:', data.battery_level));

// Move forward
fetch('http://localhost:8000/api/move?direction=forward&speed=50', {
  method: 'POST'
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### cURL

```bash
# Get status
curl http://localhost:8000/api/status

# Move forward
curl -X POST "http://localhost:8000/api/move?direction=forward&speed=50"

# Stop
curl -X POST "http://localhost:8000/api/move?direction=stop"
```

## Future Enhancements

- WebSocket support for real-time updates
- Authentication and authorization
- Rate limiting
- Sensor data endpoints
- Video streaming endpoints
- Battery alerts
- Movement history logging
