import pytest
import tempfile
import os
from pathlib import Path

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)

@pytest.fixture
def sample_config():
    """Return a sample configuration dictionary."""
    return {
        "channels": {
            "ch1": {
                "enabled": True,
                "coupling": 0,
                "volts_per_division": 5,
                "probe_multiplier": 1
            },
            "ch2": {
                "enabled": True,
                "coupling": 0,
                "volts_per_division": 5,
                "probe_multiplier": 1
            }
        },
        "timebase": {
            "time_scale": 0.0001,
            "trigger_channel": 1,
            "trigger_slope": 0
        },
        "measurement": {
            "buffer_length": 1024,
            "read_every_sample": 1,
            "num_snapshots": 10
        }
    }

@pytest.fixture
def sample_db_config():
    """Return a sample database configuration dictionary."""
    return {
        "url": "https://test-elasticsearch:9200",
        "username": "test_user",
        "password": "test_pass",
        "verify_ssl": False
    }

@pytest.fixture
def mock_oscilloscope_data():
    """Return a sample OscilloscopeData object."""
    from datetime import datetime, timezone
    from pyhtklib.lib.dtos import OscilloscopeData
    
    return OscilloscopeData(
        timestamp=datetime.now(timezone.utc),
        resolution=1024,
        channel="ch1",
        values=[1.0] * 1023
    ) 