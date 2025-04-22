import pytest
from pyhtklib.lib.dtos import OscilloscopeData
from datetime import datetime, timezone
import tempfile
import os

def test_oscilloscope_data_creation():
    """Test creation of OscilloscopeData objects."""
    # Create test data
    timestamp = datetime.now(timezone.utc)
    resolution = 1024
    channel = "ch1"
    values = [1.0, 2.0, 3.0] * 341  # 1023 values
    
    # Create data object
    data = OscilloscopeData(
        timestamp=timestamp,
        resolution=resolution,
        channel=channel,
        values=values
    )
    
    # Verify data
    assert data.timestamp == timestamp
    assert data.resolution == resolution
    assert data.channel == channel
    assert len(data.values) == resolution - 1  # -1 because resolution includes timestamp

def test_data_validation():
    """Test data validation in OscilloscopeData."""
    # Test with valid data
    valid_data = OscilloscopeData(
        timestamp=datetime.now(timezone.utc),
        resolution=1024,
        channel="ch1",
        values=[1.0] * 1023
    )
    assert valid_data.is_valid() is True
    
    # Test with invalid resolution
    invalid_resolution_data = OscilloscopeData(
        timestamp=datetime.now(timezone.utc),
        resolution=0,  # Invalid resolution
        channel="ch1",
        values=[1.0] * 1023
    )
    assert invalid_resolution_data.is_valid() is False
    
    # Test with invalid channel
    invalid_channel_data = OscilloscopeData(
        timestamp=datetime.now(timezone.utc),
        resolution=1024,
        channel="invalid_channel",  # Invalid channel
        values=[1.0] * 1023
    )
    assert invalid_channel_data.is_valid() is False

def test_data_to_csv(tmp_path):
    """Test converting OscilloscopeData to CSV format."""
    # Create test data
    timestamp = datetime.now(timezone.utc)
    data = OscilloscopeData(
        timestamp=timestamp,
        resolution=1024,
        channel="ch1",
        values=[1.0, 2.0, 3.0] * 341  # 1023 values
    )
    
    # Create output file
    output_file = tmp_path / "test_output.csv"
    
    # Write data to CSV
    data.to_csv(str(output_file))
    
    # Verify file was created and contains correct data
    assert output_file.exists()
    with open(output_file, 'r') as f:
        content = f.read()
        assert str(timestamp) in content
        assert "ch1" in content
        assert "1.0" in content

def test_data_batch_processing():
    """Test processing batches of OscilloscopeData."""
    # Create test batch
    batch = []
    for i in range(5):
        data = OscilloscopeData(
            timestamp=datetime.now(timezone.utc),
            resolution=1024,
            channel=f"ch{i%2 + 1}",  # Alternate between ch1 and ch2
            values=[float(i)] * 1023
        )
        batch.append(data)
    
    # Verify batch processing
    assert len(batch) == 5
    assert all(isinstance(d, OscilloscopeData) for d in batch)
    assert all(d.is_valid() for d in batch)
    
    # Verify channel distribution
    ch1_count = sum(1 for d in batch if d.channel == "ch1")
    ch2_count = sum(1 for d in batch if d.channel == "ch2")
    assert ch1_count + ch2_count == len(batch) 