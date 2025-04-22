import time
import schedule
import os
import json
from typing import List, Dict, Any, Tuple, Optional, Union
from venv import logger
from datetime import datetime as dt, timezone
import argparse

from ..lib.dtos import DataStore, InitializationException, RuntimeException
from .core import Oscilloscope
from .data import OscilloscopeData


oscilloscope = Oscilloscope()

def _measurement_task():
    try:
        logger.info("Executing scheduled measurement_task...")
        now = dt.now(timezone.utc)
        DataStore.timestamp_start_mesurement_task = now
        
        # Initialize oscilloscope if needed
        if not DataStore.oscillo.init_ok:
            if not oscilloscope.initialize():
                logger.error("Failed to initialize oscilloscope. Stopping the program.")
                import sys
                sys.exit(1)  # Exit with error code 1
        
        # Collect measurements
        batches = oscilloscope.collect_measurements(DataStore.oscillo.n_snapshots)
        if not batches:
            logger.error("No measurements collected!")
            return
            
        # Process data (write to files and send to database)
        oscilloscope.process_data(batches)
        
    except InitializationException as ie:
        # This exception is caught/raised when oscilo returns 0 in initialization process
        # if such event happens, whole program is terminated with the information to restart the program.
        logger.error(str(ie), exc_info=True)
        # stop_event.set()  # ! Setting stop event will force application to stop
    except RuntimeException as re:
        # This exception is caught/raised when oscilo returns 0 in measure process meaning it went/is down
        # if down, initialization of oscilo will be triggered.
        logger.warning(str(re))
    except Exception as e:
        logger.error(str(e), exc_info=True)
    
    logger.info("Finished measurement_task")
    return


def parse_configurations() -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    """
    Parse command line arguments and load configuration files.
    
    Returns:
        Tuple[Optional[str], Optional[Dict[str, Any]]]: 
            (config_file_path, database_settings_dict)
    """
    # Set up argument parser for custom config file
    parser = argparse.ArgumentParser(description="Oscilloscope Data Acquisition")
    parser.add_argument("--config", type=str, help="Path to custom configuration file")
    parser.add_argument("--db-config", type=str, help="Path to database configuration file")
    args = parser.parse_args()
    
    config_file = None
    db_settings = None
    
    # If custom config file provided, use it
    if args.config and os.path.exists(args.config):
        config_file = args.config
        logger.info(f"Using custom configuration from {args.config}")
    
    # If custom database config file provided, use it
    if args.db_config and os.path.exists(args.db_config):
        try:
            with open(args.db_config, 'r') as file:
                db_settings = json.load(file)
            logger.info(f"Using custom database settings from {args.db_config}")
        except Exception as e:
            logger.error(f"Error loading database settings: {str(e)}")
            
    return config_file, db_settings


def measurement_job(config_file=None, db_config=None, validate_db=True):
    """
    Start the measurement job with specified configuration.
    
    Args:
        config_file (str, optional): Path to a custom measurement configuration file
        db_config (Union[str, dict], optional): Either a path to database configuration file
            or a dictionary containing database settings
        validate_db (bool): Whether to validate database settings. Defaults to True.
        
    Returns:
        bool: True if all configurations were set successfully, False otherwise
    """
    logger.info("Starting measurement job...")
    
    # If no configurations are provided, try to parse them from command line
    if config_file is None and db_config is None:
        config_file, db_config = parse_configurations()
    
    # Make sure configs are set before starting measurements
    if config_file:
        if not oscilloscope.set_custom_config(config_file):
            logger.error("Failed to set measurement configuration. Exiting.")
            return False
    
    if db_config:
        # If db_config is a file path, load it
        if isinstance(db_config, str):
            try:
                with open(db_config, 'r') as file:
                    db_settings = json.load(file)
            except Exception as e:
                logger.error(f"Error loading database settings from {db_config}: {str(e)}")
                return False
        else:
            db_settings = db_config
            
        if not oscilloscope.set_database_settings(db_settings):
            logger.error("Failed to set database configuration. Exiting.")
            return False
    
    # If database settings aren't already configured, validate the default settings
    if validate_db and not oscilloscope.validate_database_settings():
        logger.error("Database settings are not valid. Please configure database settings before running measurements.")
        return False
    
    # Run the measurement task immediately
    try:
        _measurement_task()
        return True
    except Exception as e:
        logger.error(f"Error during measurement task: {str(e)}")
        return False

# def heartbeat_job():
#     logger.info("Starting heartbeat job...")
#     # Add the code for your heartbeat job here
#     logger.info("Heartbeat job completed.")