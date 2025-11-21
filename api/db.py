"""
Database connection module - NO PASSWORD REQUIRED

PostgreSQL is configured with POSTGRES_HOST_AUTH_METHOD=trust
This means NO PASSWORD authentication is needed
"""

import psycopg2
import os
import logging

logger = logging.getLogger(__name__)

def get_db_connection():
    """
    Get PostgreSQL database connection

    NO PASSWORD REQUIRED - trust mode enabled
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'sbml_models'),
            user=os.getenv('DB_USER', 'sbml')
            # NO PASSWORD PARAMETER - trust mode handles authentication
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise

def init_db():
    """Initialize database schema if not exists"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Create models table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS models (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                sbml_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create components table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS components (
                id SERIAL PRIMARY KEY,
                model_id INTEGER REFERENCES models(id) ON DELETE CASCADE,
                name VARCHAR(255) NOT NULL,
                type VARCHAR(50) NOT NULL,
                properties JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create simulations table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS simulations (
                id SERIAL PRIMARY KEY,
                model_id INTEGER REFERENCES models(id) ON DELETE CASCADE,
                config JSONB,
                results JSONB,
                status VARCHAR(50) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        """)

        conn.commit()
        cur.close()
        conn.close()

        logger.info("✅ Database schema initialized successfully (NO PASSWORD)")

    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        raise

def test_connection():
    """Test database connection - NO AUTH"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        logger.info("✅ Database connection test successful (NO PASSWORD REQUIRED)")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection test failed: {e}")
        return False

if __name__ == '__main__':
    # Test connection when run directly
    logging.basicConfig(level=logging.INFO)
    if test_connection():
        print("✅ Database connection working - NO PASSWORD NEEDED")
        init_db()
    else:
        print("❌ Database connection failed")
