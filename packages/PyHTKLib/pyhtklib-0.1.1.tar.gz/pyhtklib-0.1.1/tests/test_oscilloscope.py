import pytest
from pyhtklib import Oscilloscope
from pyhtklib.lib.constants import ES_PASSWORD, ES_USERNAME
from pyhtklib.lib.dtos import OscilloscopeData

def test_oscilloscope_initialization():
    """Test that Oscilloscope can be initialized."""
    scope = Oscilloscope()
    assert scope is not None

def test_set_custom_config(tmp_path):
    """Test setting custom configuration."""
    scope = Oscilloscope()
    
    # Create a temporary config file
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text("""
channels:
  ch1:
    enabled: true
    coupling: 0
    volts_per_division: 5
    probe_multiplier: 1
timebase:
  time_scale: 0.0001
  trigger_channel: 1
  trigger_slope: 0
measurement:
  buffer_length: 1024
  read_every_sample: 1
  num_snapshots: 10
""")
    
    # Test setting the config
    assert scope.set_custom_config(str(config_file)) is True

def test_database_settings():
    """Test database settings management."""
    scope = Oscilloscope()
    
    # Test setting database settings
    db_settings = {
        "url": "https://test-elasticsearch:9200",
        "username": "test_user",
        "password": "test_pass"
    }
    assert scope.set_database_settings(db_settings) is True
    
    # Test getting database settings
    retrieved_settings = scope.get_database_settings()
    assert retrieved_settings["url"] == db_settings["url"]
    assert retrieved_settings["username"] == db_settings["username"]

@pytest.mark.skip(reason="Database validation needs to be implemented")
def test_validate_database_settings():
    """Test database settings validation."""
    scope = Oscilloscope()
    
    # Test with valid settings
    valid_settings = {
        "url": "https://test-elasticsearch:9200",
        "username": ES_USERNAME,
        "password": ES_PASSWORD
    }
    scope.set_database_settings(valid_settings)
    assert scope.validate_database_settings() is True
    
    # Test with invalid settings
    invalid_settings = {
        "url": "invalid-url",
        "username": ES_USERNAME,
        "password": ES_PASSWORD
    }
    scope.set_database_settings(invalid_settings)
    assert scope.validate_database_settings() is False

@pytest.mark.skip(reason="Requires actual hardware connection")
def test_hardware_connection():
    """Test hardware connection (requires actual oscilloscope)."""
    scope = Oscilloscope()
    assert scope.initialize() is True
    assert scope.find_devices() is True
    assert scope.connect() is True
    
    # Test device info retrieval
    device_info = scope.get_device_info()
    assert device_info is not None
    assert "FPGA Version" in device_info  # Check for FPGA Version instead of model 