# SBML Builder - API Documentation
## Zero Authentication Edition

Complete REST API reference for the SBML Builder.

---

## Base URL
```
http://localhost:5001/api
```

---

## Authentication

**NONE REQUIRED** - All endpoints are publicly accessible with no authentication.

---

## Health Check

### GET /health
Check if the API is running.

**Request**
```http
GET /api/health
```

**Response** (200 OK)
```json
{
  "status": "healthy",
  "timestamp": "2025-11-20T16:55:00Z"
}
```

---

## Models

### GET /models
List all models.

**Request**
```http
GET /api/models
```

**Response** (200 OK)
```json
{
  "models": [
    {
      "id": 1,
      "name": "Simple Toggle Switch",
      "description": "A genetic toggle switch",
      "created_at": "2025-11-20T10:00:00Z"
    }
  ]
}
```

---

### GET /models/:id
Get a specific model by ID.

**Request**
```http
GET /api/models/1
```

**Response** (200 OK)
```json
{
  "model": {
    "id": 1,
    "name": "Simple Toggle Switch",
    "description": "A genetic toggle switch",
    "created_at": "2025-11-20T10:00:00Z",
    "components": [
      {
        "id": 1,
        "name": "LacI",
        "type": "protein"
      },
      {
        "id": 2,
        "name": "TetR",
        "type": "protein"
      }
    ],
    "interactions": [
      {
        "id": 1,
        "source_id": 1,
        "target_id": 2,
        "type": "inhibition"
      }
    ]
  }
}
```

---

### POST /models
Create a new model.

**Request**
```http
POST /api/models
Content-Type: application/json

{
  "name": "Cell Cycle Model",
  "description": "Basic cell cycle regulation"
}
```

**Response** (201 Created)
```json
{
  "id": 2,
  "name": "Cell Cycle Model",
  "description": "Basic cell cycle regulation",
  "created_at": "2025-11-20T10:05:00Z"
}
```

---

### PUT /models/:id
Update an existing model.

**Request**
```http
PUT /api/models/1
Content-Type: application/json

{
  "name": "Updated Toggle Switch",
  "description": "Modified description"
}
```

**Response** (200 OK)
```json
{
  "id": 1,
  "name": "Updated Toggle Switch",
  "description": "Modified description",
  "updated_at": "2025-11-20T10:10:00Z"
}
```

---

### DELETE /models/:id
Delete a model.

**Request**
```http
DELETE /api/models/1
```

**Response** (204 No Content)

---

## Components

### GET /models/:id/components
Get all components for a model.

**Request**
```http
GET /api/models/1/components
```

**Response** (200 OK)
```json
{
  "components": [
    {
      "id": 1,
      "model_id": 1,
      "name": "LacI",
      "type": "protein"
    },
    {
      "id": 2,
      "model_id": 1,
      "name": "TetR",
      "type": "protein"
    }
  ]
}
```

---

### POST /models/:id/components
Add a component to a model.

**Request**
```http
POST /api/models/1/components
Content-Type: application/json

{
  "name": "GFP",
  "type": "protein"
}
```

**Response** (201 Created)
```json
{
  "id": 3,
  "model_id": 1,
  "name": "GFP",
  "type": "protein"
}
```

**Component Types**
- `protein` - Protein species
- `gene` - Gene
- `rna` - RNA molecule
- `metabolite` - Small molecule
- `complex` - Protein complex

---

### DELETE /models/:model_id/components/:component_id
Remove a component from a model.

**Request**
```http
DELETE /api/models/1/components/3
```

**Response** (204 No Content)

---

## Interactions

### GET /models/:id/interactions
Get all interactions for a model.

**Request**
```http
GET /api/models/1/interactions
```

**Response** (200 OK)
```json
{
  "interactions": [
    {
      "id": 1,
      "model_id": 1,
      "source_id": 1,
      "target_id": 2,
      "type": "inhibition"
    }
  ]
}
```

---

### POST /models/:id/interactions
Add an interaction to a model.

**Request**
```http
POST /api/models/1/interactions
Content-Type: application/json

{
  "source_id": 2,
  "target_id": 1,
  "type": "inhibition"
}
```

**Response** (201 Created)
```json
{
  "id": 2,
  "model_id": 1,
  "source_id": 2,
  "target_id": 1,
  "type": "inhibition"
}
```

**Interaction Types**
- `activation` - Positive regulation
- `inhibition` - Negative regulation
- `binding` - Physical interaction
- `phosphorylation` - Post-translational modification
- `dephosphorylation` - Removal of phosphate group

---

## Simulations

### POST /models/:id/simulate
Start a simulation for a model.

**Request**
```http
POST /api/models/1/simulate
Content-Type: application/json

{
  "steps": 100,
  "method": "java-advanced",
  "model_data": {
    "components": [
      {"id": "LacI", "type": "protein"},
      {"id": "TetR", "type": "protein"}
    ],
    "interactions": [
      {"source": "LacI", "target": "TetR", "type": "inhibition"},
      {"source": "TetR", "target": "LacI", "type": "inhibition"}
    ]
  }
}
```

**Response** (200 OK)
```json
{
  "simulation_id": "abc123",
  "status": "running",
  "started_at": "2025-11-20T10:15:00Z"
}
```

**Simulation Methods**
- `java-basic` - Simple ODE integration
- `java-advanced` - Advanced ODE with adaptive step size
- `stochastic` - Gillespie stochastic simulation

---

### GET /simulations/:id/status
Get simulation status.

**Request**
```http
GET /api/simulations/abc123/status
```

**Response** (200 OK)
```json
{
  "simulation_id": "abc123",
  "status": "running",
  "progress": 65,
  "current_step": 65,
  "total_steps": 100
}
```

**Status Values**
- `queued` - Waiting to start
- `running` - Currently executing
- `complete` - Finished successfully
- `failed` - Error occurred

---

### POST /simulations/:id/stop
Stop a running simulation.

**Request**
```http
POST /api/simulations/abc123/stop
```

**Response** (200 OK)
```json
{
  "simulation_id": "abc123",
  "status": "stopped"
}
```

---

### GET /simulations/:id/export/csv
Export simulation results as CSV.

**Request**
```http
GET /api/simulations/abc123/export/csv
```

**Response** (200 OK)
```json
{
  "csv": "time,LacI,TetR\n0,1.0,0.0\n1,0.9,0.1\n..."
}
```

---

## SBML Export

### GET /models/:id/export/sbml
Export model as SBML XML.

**Request**
```http
GET /api/models/1/export/sbml
```

**Response** (200 OK)
```json
{
  "filename": "model_1.xml",
  "content": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<sbml xmlns=\"http://www.sbml.org/sbml/level3/version2/core\" level=\"3\" version=\"2\">...</sbml>"
}
```

---

## WebSocket Events

The API uses Socket.IO for real-time simulation updates.

### Connection
```javascript
const socket = io('http://localhost:5001');

socket.on('connect', () => {
  console.log('Connected to simulation server');
});
```

### Events

**simulation_update**
Emitted during simulation execution with current state.

```javascript
socket.on('simulation_update', (data) => {
  // data = {
  //   time: 42,
  //   values: { LacI: 0.5, TetR: 0.5 }
  // }
});
```

**simulation_complete**
Emitted when simulation finishes.

```javascript
socket.on('simulation_complete', (data) => {
  // data = {
  //   results: {
  //     time_points: [0, 1, 2, ...],
  //     component_values: {
  //       LacI: [1.0, 0.9, 0.8, ...],
  //       TetR: [0.0, 0.1, 0.2, ...]
  //     }
  //   }
  // }
});
```

**simulation_error**
Emitted when simulation fails.

```javascript
socket.on('simulation_error', (error) => {
  // error = { message: "Simulation failed: ..." }
});
```

---

## Error Responses

All errors follow this format:

**4xx Client Errors**
```json
{
  "error": "Model not found",
  "code": "MODEL_NOT_FOUND"
}
```

**5xx Server Errors**
```json
{
  "error": "Database connection failed",
  "code": "DB_ERROR"
}
```

### Common Error Codes

| Code | Status | Description |
|------|--------|-------------|
| `MODEL_NOT_FOUND` | 404 | Model ID doesn't exist |
| `COMPONENT_NOT_FOUND` | 404 | Component ID doesn't exist |
| `INVALID_REQUEST` | 400 | Malformed request body |
| `SIMULATION_FAILED` | 500 | Simulation error |
| `DB_ERROR` | 500 | Database connection issue |

---

## Rate Limiting

**NONE** - This is a local development tool with no rate limiting.

---

## CORS

**Enabled for all origins** - CORS is configured to allow requests from any origin.

---

## Examples

### Create and Simulate a Model

```bash
# 1. Create model
curl -X POST http://localhost:5001/api/models \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Model", "description": "Test"}'

# Response: {"id": 1, ...}

# 2. Add components
curl -X POST http://localhost:5001/api/models/1/components \
  -H "Content-Type: application/json" \
  -d '{"name": "A", "type": "protein"}'

curl -X POST http://localhost:5001/api/models/1/components \
  -H "Content-Type: application/json" \
  -d '{"name": "B", "type": "protein"}'

# 3. Add interaction
curl -X POST http://localhost:5001/api/models/1/interactions \
  -H "Content-Type: application/json" \
  -d '{"source_id": 1, "target_id": 2, "type": "activation"}'

# 4. Run simulation
curl -X POST http://localhost:5001/api/models/1/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "steps": 100,
    "method": "java-advanced",
    "model_data": {
      "components": [{"id": "A", "type": "protein"}, {"id": "B", "type": "protein"}],
      "interactions": [{"source": "A", "target": "B", "type": "activation"}]
    }
  }'

# Response: {"simulation_id": "abc123", ...}

# 5. Export SBML
curl http://localhost:5001/api/models/1/export/sbml > model.xml
```

---

## Architecture

```
┌──────────────┐
│   Frontend   │  ← Browser (builder.html)
│ (Port 5001)  │
└──────┬───────┘
       │ HTTP + WebSocket
┌──────▼───────┐
│  Flask API   │  ← Python REST API
│ (Port 5001)  │
└──┬────┬────┬─┘
   │    │    │
   ▼    ▼    ▼
┌─────┐┌────┐┌──────┐
│ccapp││Java││ DB   │  ← Backend Services
│8082 ││8081││ 5432 │
└─────┘└────┘└──────┘
```

---

**NO AUTHENTICATION REQUIRED** - Direct access to all endpoints!
