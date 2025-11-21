"""
SBML Client - Interface to ccapp service
NO AUTHENTICATION REQUIRED
"""

import requests
import os
import logging

logger = logging.getLogger(__name__)

class SBMLClient:
    """Client for interacting with ccapp SBML processing engine"""

    def __init__(self):
        self.ccapp_url = os.getenv('CCAPP_URL', 'http://localhost:8080')
        # NO AUTH TOKENS
        # NO API KEYS
        # DIRECT ACCESS

    def check_health(self):
        """Check if ccapp service is running"""
        try:
            response = requests.get(f'{self.ccapp_url}/health', timeout=5)
            return response.status_code == 200
        except:
            return False

    def create_model(self, name, description=''):
        """
        Create a new SBML model
        NO AUTHENTICATION REQUIRED
        """
        try:
            response = requests.post(
                f'{self.ccapp_url}/api/models',
                json={'name': name, 'description': description}
                # NO AUTH HEADERS
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error creating model: {e}")
            raise

    def get_model(self, model_id):
        """
        Get SBML model by ID
        NO AUTHENTICATION REQUIRED
        """
        try:
            response = requests.get(
                f'{self.ccapp_url}/api/models/{model_id}'
                # NO AUTH HEADERS
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting model: {e}")
            raise

    def add_component(self, model_id, component_name, component_type='species'):
        """
        Add a component to an SBML model
        NO AUTHENTICATION REQUIRED

        Args:
            model_id: Model ID
            component_name: Name of the component
            component_type: Type (species, reaction, parameter, etc.)
        """
        try:
            response = requests.post(
                f'{self.ccapp_url}/api/models/{model_id}/components',
                json={
                    'name': component_name,
                    'type': component_type
                }
                # NO AUTH HEADERS
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error adding component: {e}")
            raise

    def add_interaction(self, model_id, source, target, interaction_type='activation'):
        """
        Add an interaction between components
        NO AUTHENTICATION REQUIRED

        Args:
            model_id: Model ID
            source: Source component name
            target: Target component name
            interaction_type: Type (activation, inhibition, etc.)
        """
        try:
            response = requests.post(
                f'{self.ccapp_url}/api/models/{model_id}/interactions',
                json={
                    'source': source,
                    'target': target,
                    'type': interaction_type
                }
                # NO AUTH HEADERS
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error adding interaction: {e}")
            raise

    def export_sbml(self, model_id):
        """
        Export model as SBML XML
        NO AUTHENTICATION REQUIRED
        """
        try:
            response = requests.get(
                f'{self.ccapp_url}/api/models/{model_id}/export/sbml'
                # NO AUTH HEADERS
            )
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Error exporting SBML: {e}")
            raise

    def validate_sbml(self, sbml_content):
        """
        Validate SBML content
        NO AUTHENTICATION REQUIRED
        """
        try:
            response = requests.post(
                f'{self.ccapp_url}/api/sbml/validate',
                data=sbml_content,
                headers={'Content-Type': 'application/xml'}
                # NO AUTH HEADERS
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error validating SBML: {e}")
            raise
