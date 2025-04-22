"""
Oscilloscope module for Hantek oscilloscope control.
"""

# Use explicit relative imports for running from source
from .core import Oscilloscope
from .jobs import measurement_job
from .data import OscilloscopeData

__all__ = ["Oscilloscope", "measurement_job", "OscilloscopeData"]
