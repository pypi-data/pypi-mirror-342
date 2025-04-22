import pytest
from unittest.mock import patch, MagicMock
from pyhtklib import measurement_job
from pyhtklib.lib.dtos import DataStore
from pyhtklib.osciloskop.data import OscilloscopeData  # Import from correct module
from datetime import datetime, timezone
import os
import tempfile
import yaml
import json

@pytest.fixture
def mock_oscilloscope():
    """Create a mock oscilloscope configuration."""
    with patch('pyhtklib.lib.dtos._DataStore') as mock:
        mock_config = MagicMock()
        mock_config.channels = ["ch1", "ch2"]
        mock_config.buffer_length = 1024
        mock_config.read_every_sample = 1
        mock_config.n_snapshots = 10
        mock_config.init_ok = True  # Add initialization status
        mock_config.measurement_interval = 1  # Add measurement interval
        mock_config.channel_name = lambda x: f"Channel {x[-1]}"  # Add channel name function
        mock.return_value.oscillo = mock_config
        mock.return_value.export.output_dir = "output"
        mock.return_value.timestamp_start_mesurement_task = datetime.now(timezone.utc)
        mock.return_value.timestamp_read_measurement_data = datetime.now(timezone.utc)
        yield mock

@pytest.fixture
def mock_snapshot_functions():
    """Mock the snapshot creation and reading functions."""
    with patch('pyhtklib.lib.snapshot._create_snapshot') as create_mock, \
         patch('pyhtklib.lib.snapshot._read_data_from_snapshot') as read_mock:
        
        def fake_read_data(i):
            data = OscilloscopeData()  # Use the correct class
            data.ch1 = [1.0] * 1024
            data.ch2 = [2.0] * 1024
            return data
        
        create_mock.return_value = None
        read_mock.side_effect = fake_read_data
        yield (create_mock, read_mock)

@pytest.fixture
def mock_oscilloscope_measure():
    """Mock the oscilloscope measure function."""
    with patch('pyhtklib.osciloskop.core.Oscilloscope.measure') as mock:
        def fake_measure(i):
            data = OscilloscopeData()  # Use the correct class
            data.ch1 = [1.0] * 1024
            data.ch2 = [2.0] * 1024
            return data
        mock.side_effect = fake_measure
        yield mock

@pytest.fixture
def mock_oscilloscope_initialize():
    """Mock the oscilloscope initialize function."""
    with patch('pyhtklib.osciloskop.core.Oscilloscope.initialize') as mock:
        mock.return_value = True
        yield mock

def test_measurement_job_with_config(tmp_path, mock_oscilloscope, mock_snapshot_functions, mock_oscilloscope_measure, mock_oscilloscope_initialize):
    """Test measurement job with custom configuration."""
    # Create a temporary config file
    config_file = tmp_path / "test_config.yaml"
    output_dir = os.path.join(str(tmp_path), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    config = {
        "oscilloscope": {
            "ch1": {
                "enabled": True,
                "coupling": 0,
                "volts_per_division": 5,
                "probe_multiplier": 1,
                "value-multiplier": 1.0
            },
            "channels-enabled": [1, 0, 0, 0],  # Only ch1 enabled
            "window": 7,
            "measurement-interval": 60,
            "n-snapshots": 10,
            "channel-mode": 1,
            "channel-mask": 0x01,
            "trigger-channel": 0,
            "trigger-slope": 0,
            "trigger-mode": 0,
            "trigger-sweep": 0,
            "trigger-voltage": 0,
            "buffer-length": 1024,
            "read-every-sample": 1,
            "yt-mode": 0
        },
        "export_dir": output_dir
    }
    
    with open(config_file, 'w') as f:
        yaml.dump(config, f)
    
    # Run measurement job
    success = measurement_job(config_file=str(config_file), validate_db=False)
    
    # Verify results
    assert success is True
    
    # Check for files in the expected directory structure
    now = datetime.now()
    month_dir = os.path.join(output_dir, now.strftime("%B"), now.strftime("%Y-%m-%d"))
    assert os.path.exists(os.path.join(month_dir, "ch1.csv"))

def test_measurement_job_with_db_config(tmp_path, mock_oscilloscope, mock_snapshot_functions, mock_oscilloscope_measure, mock_oscilloscope_initialize):
    """Test measurement job with database configuration."""
    # Create temporary config files
    config_file = tmp_path / "test_config.yaml"
    db_config_file = tmp_path / "test_db_config.json"
    output_dir = os.path.join(str(tmp_path), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    config = {
        "oscilloscope": {
            "ch1": {
                "enabled": True,
                "coupling": 0,
                "volts_per_division": 5,
                "probe_multiplier": 1,
                "value-multiplier": 1.0
            },
            "channels-enabled": [1, 0, 0, 0],  # Only ch1 enabled
            "window": 7,
            "measurement-interval": 60,
            "n-snapshots": 10,
            "channel-mode": 1,
            "channel-mask": 0x01,
            "trigger-channel": 0,
            "trigger-slope": 0,
            "trigger-mode": 0,
            "trigger-sweep": 0,
            "trigger-voltage": 0,
            "buffer-length": 1024,
            "read-every-sample": 1,
            "yt-mode": 0
        },
        "export_dir": output_dir
    }
    
    db_config = {
        "url": "https://test-elasticsearch:9200",
        "username": "test_user",
        "password": "test_pass",
        "verify_ssl": False
    }
    
    with open(config_file, 'w') as f:
        yaml.dump(config, f)
    
    with open(db_config_file, 'w') as f:
        json.dump(db_config, f)
    
    # Run measurement job
    success = measurement_job(
        config_file=str(config_file),
        db_config=str(db_config_file),
        validate_db=False
    )
    
    # Verify results
    assert success is True
    
    # Check for files in the expected directory structure
    now = datetime.now()
    month_dir = os.path.join(output_dir, now.strftime("%B"), now.strftime("%Y-%m-%d"))
    assert os.path.exists(os.path.join(month_dir, "ch1.csv"))

@pytest.mark.skip(reason="Requires actual hardware connection")
def test_measurement_job_with_hardware():
    """Test measurement job with actual hardware (requires oscilloscope)."""
    # Test running measurement job with default settings
    success = measurement_job()
    assert success is True
    
    # Test running with custom number of snapshots
    success = measurement_job(num_snapshots=5)
    assert success is True

def test_measurement_job_output_files(tmp_path, mock_oscilloscope, mock_snapshot_functions, mock_oscilloscope_measure, mock_oscilloscope_initialize):
    """Test that measurement job creates output files."""
    # Create config file
    config_file = tmp_path / "test_config.yaml"
    output_dir = os.path.join(str(tmp_path), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    config = {
        "oscilloscope": {
            "ch1": {
                "enabled": True,
                "coupling": 0,
                "volts_per_division": 5,
                "probe_multiplier": 1,
                "value-multiplier": 1.0
            },
            "ch2": {
                "enabled": True,
                "coupling": 0,
                "volts_per_division": 5,
                "probe_multiplier": 1,
                "value-multiplier": 1.0
            },
            "channels-enabled": [1, 1, 0, 0],  # ch1 and ch2 enabled
            "window": 7,
            "measurement-interval": 60,
            "n-snapshots": 10,
            "channel-mode": 2,
            "channel-mask": 0x03,
            "trigger-channel": 0,
            "trigger-slope": 0,
            "trigger-mode": 0,
            "trigger-sweep": 0,
            "trigger-voltage": 0,
            "buffer-length": 1024,
            "read-every-sample": 1,
            "yt-mode": 0
        },
        "export_dir": output_dir
    }
    
    with open(config_file, 'w') as f:
        yaml.dump(config, f)
    
    # Run measurement job
    success = measurement_job(config_file=str(config_file), validate_db=False)
    
    # Verify results
    assert success is True
    
    # Check for files in the expected directory structure
    now = datetime.now()
    month_dir = os.path.join(output_dir, now.strftime("%B"), now.strftime("%Y-%m-%d"))
    assert os.path.exists(os.path.join(month_dir, "ch1.csv"))
    assert os.path.exists(os.path.join(month_dir, "ch2.csv")) 