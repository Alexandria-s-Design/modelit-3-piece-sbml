"""
ModelIT 4-Piece SBML Builder - Flask API
Zero Authentication Edition

NO LOGIN REQUIRED
NO PASSWORDS NEEDED
NO TOKEN VALIDATION
"""

from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os
import logging

# Import our modules
from db import get_db_connection, init_db
from sbml_client import SBMLClient
from simulation_client import SimulationClient

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow all origins (local use)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize clients
sbml_client = SBMLClient()
sim_client = SimulationClient()

# NO AUTHENTICATION MIDDLEWARE
# NO @login_required DECORATORS
# NO TOKEN VALIDATION
# DIRECT ACCESS TO ALL ENDPOINTS

@app.route('/')
def index():
    """Serve the main SBML builder interface - NO AUTH"""
    return send_from_directory('frontend', 'builder.html')

@app.route('/css/<path:filename>')
def serve_css(filename):
    """Serve CSS files - NO AUTH"""
    return send_from_directory('frontend/css', filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    """Serve JavaScript files - NO AUTH"""
    return send_from_directory('frontend/js', filename)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'services': {
            'api': 'running',
            'ccapp': sbml_client.check_health(),
            'simulator': sim_client.check_health(),
            'database': 'running'
        },
        'authentication': 'DISABLED'
    })

# ===== MODEL ENDPOINTS (NO AUTH) =====

@app.route('/api/models', methods=['GET'])
def list_models():
    """List all SBML models - NO AUTH REQUIRED"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM models ORDER BY created_at DESC")
        models = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({'models': models})
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/models', methods=['POST'])
def create_model():
    """Create a new SBML model - NO AUTH REQUIRED"""
    try:
        data = request.get_json()
        model_name = data.get('name', 'Untitled Model')
        description = data.get('description', '')

        # Create model via SBML client
        model = sbml_client.create_model(model_name, description)

        # Save to database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO models (name, description, sbml_data) VALUES (%s, %s, %s) RETURNING id",
            (model_name, description, model)
        )
        model_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'id': model_id, 'name': model_name, 'sbml': model}), 201
    except Exception as e:
        logger.error(f"Error creating model: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/models/<int:model_id>', methods=['GET'])
def get_model(model_id):
    """Get a specific SBML model - NO AUTH REQUIRED"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM models WHERE id = %s", (model_id,))
        model = cur.fetchone()
        cur.close()
        conn.close()

        if not model:
            return jsonify({'error': 'Model not found'}), 404

        return jsonify({'model': model})
    except Exception as e:
        logger.error(f"Error getting model: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/models/<int:model_id>/components', methods=['POST'])
def add_component(model_id):
    """Add a component to an SBML model - NO AUTH REQUIRED"""
    try:
        data = request.get_json()
        component_name = data.get('name')
        component_type = data.get('type', 'species')

        # Add component via SBML client
        updated_model = sbml_client.add_component(model_id, component_name, component_type)

        # Update database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE models SET sbml_data = %s, updated_at = NOW() WHERE id = %s",
            (updated_model, model_id)
        )
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'success': True, 'sbml': updated_model})
    except Exception as e:
        logger.error(f"Error adding component: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/models/<int:model_id>', methods=['DELETE'])
def delete_model(model_id):
    """Delete an SBML model - NO AUTH REQUIRED"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM models WHERE id = %s", (model_id,))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error deleting model: {e}")
        return jsonify({'error': str(e)}), 500

# ===== SIMULATION ENDPOINTS (NO AUTH) =====

@app.route('/api/models/<int:model_id>/simulate', methods=['POST'])
def simulate_model(model_id):
    """Run simulation on an SBML model - NO AUTH REQUIRED"""
    try:
        data = request.get_json()
        steps = data.get('steps', 100)
        method = data.get('method', 'java-advanced')

        # Get model from database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT sbml_data FROM models WHERE id = %s", (model_id,))
        model = cur.fetchone()
        cur.close()
        conn.close()

        if not model:
            return jsonify({'error': 'Model not found'}), 404

        # Run simulation via Java engine
        results = sim_client.run_simulation(model[0], steps)

        return jsonify({'results': results})
    except Exception as e:
        logger.error(f"Error running simulation: {e}")
        return jsonify({'error': str(e)}), 500

# ===== EXPORT ENDPOINTS (NO AUTH) =====

@app.route('/api/models/<int:model_id>/export/sbml', methods=['GET'])
def export_sbml(model_id):
    """Export model as SBML file - NO AUTH REQUIRED"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name, sbml_data FROM models WHERE id = %s", (model_id,))
        model = cur.fetchone()
        cur.close()
        conn.close()

        if not model:
            return jsonify({'error': 'Model not found'}), 404

        return jsonify({
            'filename': f"{model[0]}.sbml",
            'content': model[1]
        })
    except Exception as e:
        logger.error(f"Error exporting SBML: {e}")
        return jsonify({'error': str(e)}), 500

# ===== STATIC FILE SERVING (NO AUTH) =====

@app.route('/<path:path>')
def serve_static(path):
    """Serve static frontend files - NO AUTH"""
    return send_from_directory('frontend', path)

# Initialize database on startup (Flask 3.0+ compatible)
with app.app_context():
    """Initialize database schema - NO AUTH REQUIRED"""
    init_db()
    logger.info("Database initialized")
    logger.info("🔓 AUTHENTICATION: DISABLED")
    logger.info("✅ ALL ENDPOINTS: PUBLICLY ACCESSIBLE")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
