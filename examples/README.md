# SBML Builder - Example Models

This directory contains example biological models that can be imported into the SBML Builder.

---

## Available Examples

### 1. Simple Toggle Switch (`simple-toggle.json`)
**System**: Genetic toggle switch
**Components**: 2 proteins (LacI, TetR)
**Behavior**: Bistable - system can exist in either of two stable states

**Key Features**:
- Demonstrates mutual repression
- Shows bistability in gene regulatory networks
- Initial conditions determine final state

**Use Case**: Introduction to genetic circuits and bistability

---

### 2. Cell Cycle Model (`cell-cycle.json`)
**System**: G1/S transition regulation
**Components**: 6 proteins/complexes (Cyclin E, CDK2, E2F, Rb, etc.)
**Behavior**: Positive feedback loop driving irreversible transition

**Key Features**:
- Cyclin-CDK complex formation
- Phosphorylation cascades
- Positive feedback regulation

**Use Case**: Understanding cell cycle checkpoints and cancer biology

---

### 3. Repressilator (`repressilator.json`)
**System**: Synthetic genetic oscillator
**Components**: 3 proteins (TetR, LacI, cI)
**Behavior**: Sustained oscillations

**Key Features**:
- Ring topology of mutual repression
- Demonstrates synthetic biology design principles
- Classic example from Elowitz & Leibler (Nature 2000)

**Use Case**: Learning about oscillatory gene circuits

---

## How to Use These Examples

### Method 1: API Import (via curl)
```bash
# Import simple-toggle model
curl -X POST http://localhost:5001/api/models/import \
  -H "Content-Type: application/json" \
  -d @examples/simple-toggle.json

# Import cell-cycle model
curl -X POST http://localhost:5001/api/models/import \
  -H "Content-Type: application/json" \
  -d @examples/cell-cycle.json
```

### Method 2: Web Interface
1. Start the SBML Builder: `./start.bat` (Windows) or `./start.sh` (Linux/Mac)
2. Open http://localhost:5001
3. Click "Import Model"
4. Select one of the example JSON files
5. The model will load into the builder

### Method 3: Manual Recreation
Each example includes all the information needed to recreate it manually:
1. Create a new model with the given name and description
2. Add components one by one
3. Add interactions between components
4. Set simulation parameters
5. Run simulation

---

## Understanding the JSON Format

All example files follow this structure:

```json
{
  "name": "Model Name",
  "description": "What the model represents",
  "components": [
    {
      "id": "UniqueID",
      "name": "Display Name",
      "type": "protein|gene|rna|metabolite|complex",
      "initial_value": 0.0,
      "degradation_rate": 0.01
    }
  ],
  "interactions": [
    {
      "source": "ComponentID",
      "target": "ComponentID",
      "type": "activation|inhibition|binding|phosphorylation",
      "rate": 0.1,
      "hill_coefficient": 2,
      "half_activation": 5.0
    }
  ],
  "parameters": {
    "parameter_name": value
  },
  "simulation_config": {
    "method": "java-advanced|java-basic|stochastic",
    "steps": 100,
    "t_start": 0.0,
    "t_end": 100.0
  }
}
```

---

## Modifying Examples

Feel free to modify these examples to explore different behaviors:

**Toggle Switch Modifications**:
- Change initial values to see different stable states
- Adjust hill coefficients to change sensitivity
- Modify degradation rates to change time scales

**Cell Cycle Modifications**:
- Add growth factors or checkpoint proteins
- Include DNA damage response pathways
- Model different phases of the cell cycle

**Repressilator Modifications**:
- Change number of genes (4-gene, 5-gene oscillators)
- Adjust production/degradation rates to change period
- Add noise to explore stochastic behavior

---

## Expected Results

### Simple Toggle Switch
- **Deterministic**: System reaches one of two stable states
- **Stochastic**: May switch between states with low probability
- **Time to steady state**: ~100-200 time units

### Cell Cycle Model
- **Deterministic**: Gradual increase in Cyclin E-CDK2, sudden activation of E2F
- **Behavior**: Threshold-like response (switch-like)
- **Time to S phase entry**: ~500-800 time units

### Repressilator
- **Deterministic**: Sustained oscillations in all three proteins
- **Period**: ~100-200 time units (depends on parameters)
- **Stochastic**: Noisy oscillations with varying amplitude

---

## Creating Your Own Examples

To create your own example model:

1. **Design the network**:
   - Decide on components and their types
   - Define interactions between components
   - Set initial conditions

2. **Create JSON file**:
   - Follow the structure shown above
   - Include clear descriptions and notes

3. **Test the model**:
   - Import into SBML Builder
   - Run simulations with different parameters
   - Verify expected behavior

4. **Document**:
   - Add notes field explaining biological context
   - Include references if based on published models
   - Describe expected simulation results

---

## References

- **Toggle Switch**: Gardner et al., Nature 2000
- **Repressilator**: Elowitz & Leibler, Nature 2000
- **Cell Cycle**: Tyson & Novak, Nature Reviews MCB 2008

---

**NO AUTHENTICATION REQUIRED** - All examples work immediately!
