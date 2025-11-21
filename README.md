# SBML Model Builder - Zero Authentication Edition

**Build, simulate, and export SBML models with ZERO authentication required**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![No Auth](https://img.shields.io/badge/auth-NONE-red.svg)](README.md)

## 🔓 Zero Authentication Design

This is a **completely authentication-free** SBML modeling platform designed for:
- **Local/offline use only**
- **No usernames or passwords**
- **No login screens**
- **No database authentication**
- **Direct access to all features**
- **Maximum privacy - your models never leave your computer**

## ✨ Features

- **🔬 SBML Model Building** - Create biological models using SBML standard
- **📊 Interactive Graph Visualization** - Real-time Cytoscape.js network graph
- **⚡ Advanced Simulation** - Java-based deterministic and stochastic simulation
- **📈 Real-time Results** - Live chart updates during simulation
- **💾 Export Options** - SBML XML, CSV data, PNG graphics
- **🔄 Component Management** - Add species, reactions, parameters, compartments
- **🔗 Interaction Modeling** - Activation, inhibition, catalysis relationships

## 🏗️ Architecture

### 4-Service Docker Setup (All No-Auth)

```
┌─────────────────────────────────────────────┐
│  Builder UI (http://localhost:5000)         │
│  NO LOGIN REQUIRED                          │
└─────────────┬───────────────────────────────┘
              │
    ┌─────────▼─────────┐
    │  Flask API        │
    │  Port 5000        │
    │  NO AUTH          │
    └─────────┬─────────┘
              │
    ┌─────────┼─────────────────┐
    │         │                 │
┌───▼───┐ ┌──▼────┐ ┌─────────▼────┐
│ ccapp │ │  app  │ │  PostgreSQL  │
│ 8082  │ │ 8081  │ │    5432      │
│ SBML  │ │  Sim  │ │   NO PASSWD  │
└───────┘ └───────┘ └──────────────┘
```

### Services

1. **ccapp** - SBML Processing Engine
   - Port: 8082
   - AUTH_ENABLED=false
   - Handles SBML creation, validation, export

2. **app** - Java Simulation Engine
   - Port: 8081
   - OPEN_ACCESS=true
   - Runs deterministic and stochastic simulations

3. **db** - PostgreSQL Database
   - Port: 5432
   - POSTGRES_HOST_AUTH_METHOD=trust (NO PASSWORD)
   - Stores models and simulation results

4. **api** - Flask API + Frontend
   - Port: 5000
   - NO_AUTH=true
   - Serves UI and provides REST API

## 🚀 Quick Start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- That's it! No accounts, no sign-ups, no configuration.

### Installation

```bash
# Clone the repository
git clone https://github.com/Alexandria-s-Design/modelit-3-piece-sbml.git
cd modelit-3-piece-sbml

# Start services (Windows)
start.bat

# OR Start services (Linux/Mac)
./start.sh
```

**Your browser will automatically open to http://localhost:5000**

NO USERNAME. NO PASSWORD. Just build.

### Stopping Services

```bash
# Windows
stop.bat

# Linux/Mac
./stop.sh
```

## 📖 Usage

### Creating Your First Model

1. **Open http://localhost:5000** (automatically opens on startup)
2. **Enter model name and description** in the "Current Model" panel
3. **Click "Save Model"**
4. **Add components:**
   - Enter component name (e.g., "Protein_A")
   - Select type (Species, Reaction, Parameter, Compartment)
   - Click "Add Component"
5. **Add interactions:**
   - Select source component
   - Select target component
   - Choose interaction type (Activation, Inhibition, Catalysis)
   - Click "Add Interaction"
6. **View your model** in the interactive graph

### Running Simulations

1. **Configure simulation:**
   - Set time steps (default: 100)
   - Choose method:
     - Java (Advanced) - Deterministic ODE solver
     - Java (Stochastic) - Gillespie algorithm
     - Euler - Simple numerical integration
     - Runge-Kutta - Higher-order integration
2. **Click "Run Simulation"**
3. **Watch real-time results** in the chart
4. **Click "Stop"** to halt simulation

### Exporting

- **Export SBML** - Download as .xml file
- **Export CSV** - Download simulation results as .csv
- **Export Graph PNG** - Download network visualization

## 🔧 Configuration

All configuration is in `.env.example`. Copy to `.env` if you need to customize:

```bash
# Example: Change API port
API_PORT=5001

# Example: Change database name
DB_NAME=my_custom_db

# Authentication is ALWAYS disabled
AUTH_ENABLED=false
NO_AUTH=true
```

## 📁 Project Structure

```
modelit-3-piece-sbml/
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py              # Flask API (NO AUTH)
│   ├── db.py               # Database connection (NO PASSWORD)
│   ├── sbml_client.py      # ccapp interface
│   └── simulation_client.py # Java sim interface
├── frontend/
│   ├── builder.html        # Main UI (NO LOGIN FORM)
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── builder.js      # Component management
│       ├── graph.js        # Cytoscape visualization
│       └── simulation.js   # Chart.js + Socket.IO
├── docs/
│   ├── QUICKSTART.md
│   ├── API.md
│   └── JAVA_SIMULATION.md
├── examples/
│   ├── simple-toggle.json
│   └── cell-cycle.json
├── docker-compose.yml      # 4-service setup
├── start.bat / start.sh    # Windows/Linux startup
├── stop.bat / stop.sh      # Shutdown scripts
├── .env.example            # Configuration template
└── README.md               # This file
```

## 🔬 Advanced Usage

### Custom Simulation Methods

The Java simulation engine supports multiple algorithms:

- **Deterministic (ODE)** - Continuous, precise for large populations
- **Stochastic (Gillespie)** - Discrete, realistic for small populations
- **Euler Method** - Fast, less accurate
- **Runge-Kutta** - Slower, more accurate

### Batch Operations

Use the REST API directly for automation:

```bash
# Create model
curl -X POST http://localhost:5000/api/models \
  -H "Content-Type: application/json" \
  -d '{"name": "My Model", "description": "Test"}'

# Add component
curl -X POST http://localhost:5000/api/models/1/components \
  -H "Content-Type: application/json" \
  -d '{"name": "ProteinA", "type": "species"}'
```

NO API KEYS. NO TOKENS. Just HTTP.

## 🛠️ Troubleshooting

### Port Conflict

If port 5000 is in use, edit `docker-compose.yml`:

```yaml
api:
  ports:
    - "5001:5000"  # Change to any available port
```

### Database Connection Issues

The database uses **trust authentication mode** (no password). If you see connection errors:

```bash
# Check if database is running
docker-compose ps

# View database logs
docker-compose logs db

# Restart services
docker-compose restart
```

### Simulation Not Starting

Check that all services are healthy:

```bash
# Check service status
curl http://localhost:5000/health

# Should return:
# {
#   "status": "healthy",
#   "services": {
#     "api": "running",
#     "ccapp": true,
#     "simulator": true,
#     "database": "running"
#   },
#   "authentication": "DISABLED"
# }
```

## 📚 Documentation

- [Quick Start Guide](docs/QUICKSTART.md) - Step-by-step tutorial
- [API Reference](docs/API.md) - Complete REST API documentation
- [Java Simulation](docs/JAVA_SIMULATION.md) - Advanced simulation features

## 🔒 Security Note

**This system is designed for LOCAL USE ONLY.**

- **No authentication** means anyone with network access can use it
- **Do NOT expose to the internet** without adding authentication
- **Perfect for:** Local development, offline modeling, privacy-focused work
- **Not suitable for:** Public servers, multi-user environments, production

## 🤝 Contributing

Contributions welcome! This is an open-source project.

```bash
# Fork the repository
# Create a feature branch
git checkout -b feature/my-feature

# Make changes and commit
git commit -m "Add my feature"

# Push to GitHub
git push origin feature/my-feature

# Open a Pull Request
```

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- **ModelIT** - Original SBML modeling platform
- **Cell Collective** - Biological modeling framework
- **Cytoscape.js** - Network visualization library
- **Chart.js** - Real-time charting
- **Flask** - Python web framework
- **PostgreSQL** - Database engine

## 📞 Support

Found a bug? Have a question?

- Open an [Issue](https://github.com/Alexandria-s-Design/modelit-3-piece-sbml/issues)
- Check [Documentation](docs/)
- Review [Examples](examples/)

---

**Built for simplicity. Built for privacy. Built for YOU.**

🔓 **NO AUTH. NO LIMITS.**
