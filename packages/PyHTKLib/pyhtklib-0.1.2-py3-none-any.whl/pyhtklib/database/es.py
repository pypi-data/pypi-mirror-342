"""
Elasticsearch integration for storing oscilloscope data.
"""
from datetime import timezone
from typing import List, Dict, Any, Tuple, Optional
import uuid
import warnings
from venv import logger

# Suppress Elasticsearch warnings
warnings.filterwarnings("ignore", category=UserWarning, module="elasticsearch")

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from datetime import datetime as dt

# Internal relative imports
from pyhtklib.lib.constants import API_KEY, ES_PASSWORD, ES_USERNAME, GET_ES_OSICLLO_DATA_INDEX
from ..osciloskop.data import OscilloscopeData

# Default database settings
_es_settings = {
    "url": "https://localhost:9200",
    "username": ES_USERNAME,
    "password": ES_PASSWORD,
    "timeout": 300,
    "api_key": API_KEY,
    "use_api_key": False,
    "verify_ssl": False,
    "retry_on_timeout": True,
    "max_retries": 3
}

def set_database_settings(settings: Dict[str, Any]) -> bool:
    """
    Update the Elasticsearch connection settings.
    
    Args:
        settings (dict): Dictionary containing database connection settings.
            Possible keys:
            - url: Elasticsearch server URL
            - username: Username for authentication
            - password: Password for authentication
            - timeout: Connection timeout in seconds
            - api_key: API key for authentication
            - use_api_key: Whether to use API key instead of username/password
            - verify_ssl: Whether to verify SSL certificates
            - retry_on_timeout: Whether to retry on connection timeout
            - max_retries: Maximum number of retry attempts
    
    Returns:
        bool: True if settings were successfully updated
    """
    global _es_settings
    if not settings:
        logger.warning("Empty database settings provided. Using defaults.")
        return False
        
    # Update only provided settings
    for key, value in settings.items():
        if key in _es_settings:
            _es_settings[key] = value
            logger.info(f"Updated database setting: {key}")
    
    logger.info(f"Database settings updated. URL: {_es_settings['url']}")
    return True

def create_client() -> Elasticsearch:
    """
    Create an Elasticsearch client with current settings.
    
    Returns:
        Elasticsearch: Configured Elasticsearch client
    """
    global _es_settings
    
    # Configure Elasticsearch client based on settings
    es_params = {
        "hosts": _es_settings["url"],
        "timeout": _es_settings["timeout"],
        "verify_certs": _es_settings["verify_ssl"],
        "retry_on_timeout": _es_settings["retry_on_timeout"],
        "max_retries": _es_settings["max_retries"]
    }
    
    # Choose authentication method
    if _es_settings["use_api_key"] and _es_settings["api_key"]:
        es_params["api_key"] = _es_settings["api_key"]
    elif _es_settings["username"] and _es_settings["password"]:
        es_params["http_auth"] = (_es_settings["username"], _es_settings["password"])
    
    return Elasticsearch(**es_params)

def test_connection() -> bool:
    """
    Test the connection to Elasticsearch.
    
    Returns:
        bool: True if connection is successful
    """
    try:
        es = create_client()
        return es.ping()
    except Exception as e:
        logger.error(f"Error connecting to Elasticsearch: {str(e)}")
        return False

def _bulk_measured_data(data: List[OscilloscopeData]) -> Tuple[bool, Optional[str]]:
    """
    Send measured oscilloscope data to Elasticsearch using bulk operations.
    
    Args:
        data: List of oscilloscope data objects
        
    Returns:
        tuple: (success, bulk_id) tuple indicating success and operation ID
    """
    if not data:
        logger.warning("No data to send.")
        return False, None

    try:
        es = create_client()
        
        bulk_data = []
        now = dt.now(timezone.utc)
        bulk_id = str(uuid.uuid4())

        # Prepare bulk data from all batches
        for batch in data:
            bulk_data.extend(batch.serialize_bulk_data_for_all_channels(bulk_id))
            
        if not bulk_data:
            logger.warning("No data to send in bulk operation.")
            return False, None

        # Execute bulk operation with error handling
        try:
            success, failed = bulk(es, bulk_data)
            
            if success:
                logger.info(f"✔ Bulk data sent to ES (bulk_id={bulk_id}, documents={success})")
                return True, bulk_id
            else:
                logger.error(f"❌ Error sending bulk data: {failed}")
                return False, bulk_id
                
        except Exception as e:
            logger.error(f"❌ Error during bulk operation: {str(e)}")
            return False, bulk_id
            
    except Exception as e:
        logger.error(f"❌ Error setting up Elasticsearch client: {str(e)}")
        return False, None
