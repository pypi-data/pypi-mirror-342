#!/usr/bin/env python
"""
Entry point for the PyHTKLib library.
"""
import logging
from src.pyhtklib.osciloskop.jobs import measurement_job



# Configure logging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    # Library entry point
    measurement_job()

