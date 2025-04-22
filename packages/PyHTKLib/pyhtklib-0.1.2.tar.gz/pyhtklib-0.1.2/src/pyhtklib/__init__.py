"""
PyHTKLib - Python library for Hantek oscilloscope control and data acquisition
"""

__version__ = "0.1.0"

# Use explicit relative imports
from .osciloskop.core import Oscilloscope
from .osciloskop.jobs import measurement_job

__all__ = ["Oscilloscope", "measurement_job"] 