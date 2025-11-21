# SBML Builder - Java Simulation Engine
## Advanced Simulation Features

The Java simulation engine provides high-performance numerical simulation of SBML models.

---

## Overview

The Java simulator (running on port 8081) provides:
- **Deterministic Simulation**: ODE integration with adaptive step size
- **Stochastic Simulation**: Gillespie algorithm for discrete events
- **Real-time Updates**: WebSocket communication for live results
- **High Performance**: Optimized Java implementation

---

## Simulation Methods

### 1. Basic ODE Integration (`java-basic`)

Simple Euler method for ordinary differential equations.

**Use Case**
- Quick simulations
- Educational purposes
- Simple models

**Algorithm**
```
For each timestep:
  dx/dt = f(x, t)
  x(t+1) = x(t) + dt * dx/dt
```

**Example**
```json
{
  "method": "java-basic",
  "steps": 100,
  "dt": 0.1
}
```

**Pros**
- Fast execution
- Simple to understand
- Low memory usage

**Cons**
- Fixed step size
- Less accurate for stiff systems
- May require very small timesteps

---

### 2. Advanced ODE Integration (`java-advanced`)

Adaptive Runge-Kutta method with error control.

**Use Case**
- Production simulations
- Complex models
- Stiff systems

**Algorithm**
- 4th/5th order Runge-Kutta (RK45)
- Adaptive step size control
- Error estimation and tolerance

**Example**
```json
{
  "method": "java-advanced",
  "steps": 100,
  "tolerance": 1e-6,
  "max_step": 1.0,
  "min_step": 1e-8
}
```

**Pros**
- High accuracy
- Adaptive step size
- Handles stiff systems
- Optimal performance

**Cons**
- Slightly slower than basic
- More complex algorithm

---

### 3. Stochastic Simulation (`stochastic`)

Gillespie's Direct Method for discrete stochastic simulation.

**Use Case**
- Low molecule counts
- Noisy biological systems
- Single-cell behavior

**Algorithm**
```
While t < t_max:
  1. Calculate propensities for all reactions
  2. Calculate total propensity
  3. Draw random time to next reaction
  4. Select which reaction fires
  5. Update species counts
  6. Advance time
```

**Example**
```json
{
  "method": "stochastic",
  "steps": 1000,
  "seed": 42,
  "num_trajectories": 10
}
```

**Pros**
- Accurate for small populations
- Captures stochastic noise
- Exact algorithm (not approximate)

**Cons**
- Slower for large populations
- Requires many trajectories
- Results vary between runs

---

## Configuration Parameters

### Common Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `method` | string | `java-advanced` | Simulation method |
| `steps` | int | 100 | Number of output steps |
| `t_start` | float | 0.0 | Start time |
| `t_end` | float | 100.0 | End time |

### ODE-Specific Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `tolerance` | float | 1e-6 | Error tolerance |
| `max_step` | float | 1.0 | Maximum step size |
| `min_step` | float | 1e-8 | Minimum step size |
| `dt` | float | 0.1 | Fixed step size (basic only) |

### Stochastic-Specific Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `seed` | int | random | Random seed |
| `num_trajectories` | int | 1 | Number of runs |
| `reactions_per_step` | int | auto | Events between outputs |

---

## Model Format

The Java simulator accepts models in this format:

```json
{
  "components": [
    {
      "id": "A",
      "type": "protein",
      "initial_value": 100.0
    },
    {
      "id": "B",
      "type": "protein",
      "initial_value": 0.0
    }
  ],
  "interactions": [
    {
      "source": "A",
      "target": "B",
      "type": "activation",
      "rate": 0.1
    }
  ],
  "parameters": {
    "degradation_A": 0.01,
    "degradation_B": 0.02
  }
}
```

---

## Component Types

Each component type has default properties:

### Protein
```json
{
  "type": "protein",
  "degradation_rate": 0.01,
  "translation_rate": 1.0
}
```

### Gene
```json
{
  "type": "gene",
  "transcription_rate": 0.1,
  "copy_number": 1
}
```

### RNA
```json
{
  "type": "rna",
  "degradation_rate": 0.1,
  "translation_rate": 1.0
}
```

### Metabolite
```json
{
  "type": "metabolite",
  "diffusion_rate": 0.5
}
```

---

## Interaction Types

### Activation
```
rate = k * [source] * Hill(target, K, n)
```

**Parameters**
- `k`: Rate constant
- `K`: Half-activation constant
- `n`: Hill coefficient

### Inhibition
```
rate = k * [source] / (1 + ([target]/K)^n)
```

### Binding
```
source + target ⇌ complex
forward_rate * [source] * [target]
reverse_rate * [complex]
```

### Phosphorylation
```
source + target → source + target_P
rate = k * [source] * [target]
```

---

## Real-time Communication

### WebSocket Protocol

The simulator emits updates via Socket.IO:

```javascript
// Connect to simulator
const socket = io('http://localhost:5001');

// Listen for updates
socket.on('simulation_update', (data) => {
  console.log('Time:', data.time);
  console.log('Values:', data.values);
});

socket.on('simulation_complete', (results) => {
  console.log('Simulation finished');
  console.log(results);
});
```

### Update Frequency

Updates are sent every N steps, where N depends on:
- Total simulation steps
- Network latency
- Client processing speed

Default: Update every `max(1, steps/100)` steps

---

## Performance Optimization

### For Large Models (>100 components)

1. **Use `java-advanced`**: Better scaling than basic
2. **Increase tolerance**: `1e-4` instead of `1e-6`
3. **Reduce output steps**: Only save necessary data points
4. **Disable real-time updates**: Process results at end

```json
{
  "method": "java-advanced",
  "tolerance": 1e-4,
  "steps": 1000,
  "realtime_updates": false
}
```

### For Stochastic Simulations

1. **Parallel trajectories**: Run multiple seeds in parallel
2. **Batch processing**: Group reactions between outputs
3. **Adaptive tau-leaping**: Approximate for fast reactions

```json
{
  "method": "stochastic",
  "num_trajectories": 100,
  "parallel": true,
  "adaptive_tau": true
}
```

---

## Examples

### Example 1: Simple Production-Degradation

```json
{
  "method": "java-advanced",
  "steps": 100,
  "model_data": {
    "components": [
      {
        "id": "Protein",
        "type": "protein",
        "initial_value": 0.0
      }
    ],
    "parameters": {
      "production": 10.0,
      "degradation": 0.1
    }
  }
}
```

**Expected Result**: Protein approaches steady state of 100

---

### Example 2: Repressilator (3-gene oscillator)

```json
{
  "method": "java-advanced",
  "steps": 500,
  "t_end": 1000,
  "model_data": {
    "components": [
      {"id": "TetR", "type": "protein", "initial_value": 10},
      {"id": "LacI", "type": "protein", "initial_value": 0},
      {"id": "cI", "type": "protein", "initial_value": 0}
    ],
    "interactions": [
      {"source": "TetR", "target": "LacI", "type": "inhibition"},
      {"source": "LacI", "target": "cI", "type": "inhibition"},
      {"source": "cI", "target": "TetR", "type": "inhibition"}
    ]
  }
}
```

**Expected Result**: Oscillating concentrations of all three proteins

---

### Example 3: Stochastic Gene Expression

```json
{
  "method": "stochastic",
  "steps": 1000,
  "num_trajectories": 50,
  "seed": 123,
  "model_data": {
    "components": [
      {"id": "mRNA", "type": "rna", "initial_value": 0},
      {"id": "Protein", "type": "protein", "initial_value": 0}
    ],
    "parameters": {
      "transcription": 0.1,
      "translation": 1.0,
      "mRNA_degradation": 0.5,
      "protein_degradation": 0.05
    }
  }
}
```

**Expected Result**: Noisy protein expression with bursts

---

## Direct API Access

You can bypass the Flask API and call the Java simulator directly:

```bash
curl -X POST http://localhost:8081/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "method": "java-advanced",
    "steps": 100,
    "model": {...}
  }'
```

**Response**
```json
{
  "simulation_id": "xyz789",
  "status": "running"
}
```

Then poll for results:
```bash
curl http://localhost:8081/results/xyz789
```

---

## Error Handling

### Common Errors

**Numerical Instability**
```json
{
  "error": "Integration failed: step size too small",
  "solution": "Increase tolerance or check model equations"
}
```

**Timeout**
```json
{
  "error": "Simulation timeout after 300s",
  "solution": "Reduce simulation time or increase timeout"
}
```

**Invalid Model**
```json
{
  "error": "Undefined component: XYZ",
  "solution": "Check all component IDs are defined"
}
```

---

## Advanced Features

### Custom Equations

Define custom rate laws:

```json
{
  "custom_rates": {
    "my_reaction": "k1 * [A] * [B] / (K + [C])"
  }
}
```

### Events

Trigger changes at specific times or conditions:

```json
{
  "events": [
    {
      "time": 50.0,
      "action": "set",
      "target": "Inducer",
      "value": 100.0
    },
    {
      "condition": "[Protein] > 50",
      "action": "stop"
    }
  ]
}
```

### Multi-compartment Models

Simulate spatial organization:

```json
{
  "compartments": [
    {"id": "nucleus", "volume": 1.0},
    {"id": "cytoplasm", "volume": 10.0}
  ],
  "transport": [
    {
      "component": "mRNA",
      "from": "nucleus",
      "to": "cytoplasm",
      "rate": 0.1
    }
  ]
}
```

---

## Debugging

### Enable Verbose Logging

Set environment variable:
```bash
JAVA_SIM_DEBUG=true
```

### View Internal State

```bash
curl http://localhost:8081/debug/simulation/abc123
```

Returns:
```json
{
  "current_time": 42.5,
  "step_size": 0.01,
  "num_steps": 4250,
  "state": {
    "A": 15.3,
    "B": 8.7
  }
}
```

---

## References

- **SBML Specification**: http://sbml.org/
- **Gillespie Algorithm**: Gillespie (1977) J Comp Phys
- **Runge-Kutta Methods**: Dormand-Prince (1980)

---

**NO AUTHENTICATION REQUIRED** - Direct access to all simulation features!
