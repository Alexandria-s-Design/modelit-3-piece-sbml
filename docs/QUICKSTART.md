# SBML Builder - Quickstart Guide
## Zero Authentication Edition

Get up and running with the SBML Builder in 5 minutes!

---

## Prerequisites

- **Docker Desktop** (Windows/Mac) or **Docker** + **Docker Compose** (Linux)
- **4GB RAM** minimum
- **Ports Available**: 5001, 5432, 8081, 8082

---

## Step 1: Start the System

### Windows
```batch
start.bat
```

### Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

The startup script will:
1. Check if Docker is running
2. Build and start all 4 services
3. Initialize the database
4. Open http://localhost:5001 in your browser

---

## Step 2: Build Your First Model

### Create a Simple Toggle Switch Model

1. **Name Your Model**
   - Model Name: `Simple Toggle Switch`
   - Description: `A genetic toggle switch between two repressor proteins`

2. **Click "Save Model"**

3. **Add Components**
   - Component 1:
     - Name: `LacI`
     - Type: `protein`
     - Click "Add Component"

   - Component 2:
     - Name: `TetR`
     - Type: `protein`
     - Click "Add Component"

4. **Add Interactions**
   - Interaction 1:
     - Source: `LacI`
     - Target: `TetR`
     - Type: `inhibition`
     - Click "Add Interaction"

   - Interaction 2:
     - Source: `TetR`
     - Target: `LacI`
     - Type: `inhibition`
     - Click "Add Interaction"

You'll see the model appear in the graph visualization!

---

## Step 3: Run a Simulation

1. **Set Simulation Parameters**
   - Steps: `100`
   - Method: `java-advanced` (recommended)

2. **Click "Run Simulation"**

3. **Watch the Results**
   - Real-time graph updates via Socket.IO
   - See oscillating behavior between LacI and TetR

4. **Export Results** (optional)
   - Click "Download CSV" to save simulation data

---

## Step 4: Export Your Model

### Export as SBML (XML format)
```
Click "Export" → "SBML"
```
Downloads: `model_<id>.xml`

### Export as PNG (Graph image)
```
Click "Export" → "PNG"
```
Downloads: `model-graph.png`

---

## Quick Tips

### NO LOGIN REQUIRED
- Direct access to all features
- No username/password setup
- No authentication tokens needed

### Real-time Updates
- Graph updates as you add components
- Live simulation results via WebSocket
- Automatic database persistence

### Graph Controls
- **Drag** nodes to rearrange
- **Zoom** with mouse wheel
- **Pan** by dragging background
- **Click** nodes/edges to highlight

---

## Troubleshooting

### Port Conflicts
If you see "port already allocated" errors:

1. Check what's using the port:
   ```bash
   # Windows
   netstat -ano | findstr :5001

   # Linux/Mac
   lsof -i :5001
   ```

2. Stop the service or modify `docker-compose.yml` to use different ports

### Services Won't Start
```bash
# Check logs
docker-compose logs -f

# Restart a specific service
docker-compose restart api

# Rebuild from scratch
docker-compose down
docker-compose up -d --build
```

### Frontend Not Loading
1. Verify API is running:
   ```bash
   curl http://localhost:5001/health
   ```

2. Check browser console for errors (F12)

3. Clear browser cache

---

## Next Steps

- **API Documentation**: See `docs/API.md` for REST endpoints
- **Java Simulation**: See `docs/JAVA_SIMULATION.md` for advanced features
- **Examples**: Check `examples/` directory for sample models

---

## Stop the System

### Windows
```batch
stop.bat
```

### Linux/Mac
```bash
./stop.sh
```

This stops and removes all containers but preserves your database data.

---

## Data Persistence

Your models are automatically saved to a PostgreSQL database with persistent volume storage:
- Volume: `modelit-3-piece-sbml_db_data`
- Location: Docker volume (survives container restarts)
- No backups needed during normal operation

---

## Support

This is a zero-authentication local development tool. For production use:
1. Add authentication middleware
2. Use production WSGI server (gunicorn)
3. Enable HTTPS
4. Implement user management

---

**Happy Modeling! 🧬**
