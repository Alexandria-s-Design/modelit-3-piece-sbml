"""
Simulation Client - Interface to Java simulation engine (app service)
NO AUTHENTICATION REQUIRED
"""

import requests
import os
import logging

logger = logging.getLogger(__name__)

class SimulationClient:
    """Client for interacting with Java-based simulation engine"""

    def __init__(self):
        self.app_url = os.getenv('APP_URL', 'http://localhost:8081')
        # NO AUTH TOKENS
        # NO API KEYS
        # DIRECT ACCESS

    def check_health(self):
        """Check if simulation service is running"""
        try:
            response = requests.get(f'{self.app_url}/health', timeout=5)
            return response.status_code == 200
        except:
            return False

    def run_simulation(self, sbml_model, steps=100, config=None):
        """
        Run advanced simulation using Java engine
        NO AUTHENTICATION REQUIRED

        Args:
            sbml_model: SBML model data
            steps: Number of simulation steps
            config: Additional simulation configuration
        """
        try:
            payload = {
                'model': sbml_model,
                'steps': steps,
                'config': config or {}
            }

            response = requests.post(
                f'{self.app_url}/api/simulate',
                json=payload,
                timeout=60  # Simulations can take time
                # NO AUTH HEADERS
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error running simulation: {e}")
            raise

    def get_simulation_status(self, sim_id):
        """
        Check simulation status
        NO AUTHENTICATION REQUIRED
        """
        try:
            response = requests.get(
                f'{self.app_url}/api/simulations/{sim_id}'
                # NO AUTH HEADERS
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting simulation status: {e}")
            raise

    def get_simulation_results(self, sim_id):
        """
        Get simulation results
        NO AUTHENTICATION REQUIRED
        """
        try:
            response = requests.get(
                f'{self.app_url}/api/simulations/{sim_id}/results'
                # NO AUTH HEADERS
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting simulation results: {e}")
            raise

    def cancel_simulation(self, sim_id):
        """
        Cancel a running simulation
        NO AUTHENTICATION REQUIRED
        """
        try:
            response = requests.post(
                f'{self.app_url}/api/simulations/{sim_id}/cancel'
                # NO AUTH HEADERS
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error canceling simulation: {e}")
            raise

    def run_stochastic_simulation(self, sbml_model, runs=10, steps=100):
        """
        Run stochastic simulation (multiple runs)
        NO AUTHENTICATION REQUIRED

        Args:
            sbml_model: SBML model data
            runs: Number of stochastic runs
            steps: Steps per run
        """
        try:
            payload = {
                'model': sbml_model,
                'runs': runs,
                'steps': steps,
                'method': 'stochastic'
            }

            response = requests.post(
                f'{self.app_url}/api/simulate/stochastic',
                json=payload,
                timeout=120  # Stochastic sims take longer
                # NO AUTH HEADERS
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error running stochastic simulation: {e}")
            raise

    def get_available_methods(self):
        """
        Get list of available simulation methods
        NO AUTHENTICATION REQUIRED
        """
        try:
            response = requests.get(
                f'{self.app_url}/api/methods'
                # NO AUTH HEADERS
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting simulation methods: {e}")
            raise
