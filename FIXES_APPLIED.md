# SBML Builder - Docker Configuration Fixes

## Problem Summary

The `sbml-ccapp` service was continuously restarting with exit code 0. Investigation revealed:

1. **Missing Startup Command**: The Docker image had no default command configured
2. **Missing Environment Variables**: Django required specific environment variables for:
   - ALLOWED_HOSTS configuration
   - Database connection

## Fixes Applied

### 1. Added Django Runserver Command

**File**: `docker-compose.yml`
**Change**: Added `command` directive to ccapp service

```yaml
ccapp:
  image: modelit-codex-ccapp:latest
  container_name: sbml-ccapp
  command: python3 manage.py runserver 0.0.0.0:8080  # <- ADDED THIS LINE
  ports:
    - "8082:8080"
```

**Why**: The modelit-codex-ccapp:latest image only specified `python3` as its CMD, which exits immediately without a script to run.

### 2. Added Django Environment Configuration

**File**: `docker-compose.yml`
**Change**: Added Django-specific environment variables

```yaml
environment:
  - CC_ENVIRONMENT=development      # Django ALLOWED_HOSTS configuration
  - CC_HOST_APP_PORT=8080           # Internal Django port
  - CC_HOST_CLIENT_PORT=5001        # Client-facing API port
```

**Why**: Django's `config/settings.py` requires `CC_ENVIRONMENT` to determine ALLOWED_HOSTS:
- `development` mode adds: localhost, 127.0.0.1
- Without this variable, Django raises: `ValueError: Client allowed hosts environment type is required!`

### 3. Fixed Database Connection Variables

**File**: `docker-compose.yml`
**Change**: Renamed database environment variables to match Django expectations

```yaml
# BEFORE (incorrect variable names)
- DB_HOST=db
- DB_PORT=5432
- DB_NAME=sbml_models
- DB_USER=sbml

# AFTER (correct variable names for Django)
- POSTGRES_HOST=db                # Database connection (Django expects POSTGRES_*)
- POSTGRES_PORT=5432
- POSTGRES_DB=sbml_models
- POSTGRES_USER=sbml
- POSTGRES_PASSWORD=              # Empty password (trust auth mode)
```

**Why**: Django's database configuration in `config/settings.py` reads:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv('POSTGRES_DB'),      # Not DB_NAME
        "USER": os.getenv('POSTGRES_USER'),    # Not DB_USER
        "PASSWORD": os.getenv('POSTGRES_PASSWORD'),
        "HOST": os.getenv('POSTGRES_HOST'),    # Not DB_HOST
        "PORT": os.getenv('POSTGRES_PORT'),    # Not DB_PORT
    }
}
```

### 4. Applied Database Migrations

**Command Run**:
```bash
docker exec sbml-ccapp python3 manage.py migrate
```

**Result**: Applied 34 migrations for:
- admin, auth, contenttypes, oauth, sessions, users, xauth

**Why**: Django applications require database schema to be initialized via migrations.

## Verification

### Service Status
All 4 services are now running successfully:

```bash
$ docker ps --filter "name=sbml-"
NAMES            STATUS                   PORTS
sbml-ccapp       Up                       0.0.0.0:8082->8080/tcp
sbml-api         Up                       0.0.0.0:5001->5000/tcp
sbml-simulator   Up                       0.0.0.0:8081->8081/tcp
sbml-database    Up (healthy)             0.0.0.0:5432->5432/tcp
```

### Health Check
```bash
$ curl http://localhost:5001/health
{
  "status": "healthy",
  "authentication": "DISABLED",
  "services": {
    "api": "running",
    "database": "running",
    "ccapp": true,
    "simulator": true
  }
}
```

### Builder Interface
Accessible at: **http://localhost:5001**

Title: "SBML Builder - Zero Auth Edition"

## System Architecture (Updated)

```
┌─────────────────────────────────────────────┐
│  Builder UI (http://localhost:5001)         │
│  NO LOGIN REQUIRED - ZERO AUTH EDITION      │
└─────────────┬───────────────────────────────┘
              │
    ┌─────────▼─────────┐
    │  Flask API        │
    │  Port 5001        │
    │  NO_AUTH=true     │
    └─────────┬─────────┘
              │
    ┌─────────┼─────────────────┐
    │         │                 │
┌───▼───┐ ┌──▼────┐ ┌─────────▼────┐
│ ccapp │ │  app  │ │  PostgreSQL  │
│ 8082  │ │ 8081  │ │    5432      │
│ SBML  │ │  Sim  │ │   NO PASSWD  │
│Django │ │ Java  │ │   trust auth │
│ ✅    │ │  ✅   │ │     ✅       │
└───────┘ └───────┘ └──────────────┘
```

## Files Modified

1. **docker-compose.yml** - Added command and environment variables to ccapp service

## Files Created

1. **FIXES_APPLIED.md** - This documentation file

## Next Steps

The system is now fully operational! You can:

1. **Access the builder**: http://localhost:5001
2. **Create SBML models**: Use the web interface
3. **Run simulations**: Test with example models in `examples/` directory
4. **Import examples**: Use the API or web interface

## Troubleshooting Future Issues

If ccapp service fails again, check:

1. **Django logs**: `docker logs sbml-ccapp`
2. **Environment variables**: Ensure all CC_* and POSTGRES_* variables are set
3. **Database connectivity**: Verify db service is healthy
4. **Migrations**: Ensure all migrations are applied

---

**Fixed**: November 20, 2025
**Status**: ✅ All services operational
**Testing**: Verified via health endpoint and manual inspection
