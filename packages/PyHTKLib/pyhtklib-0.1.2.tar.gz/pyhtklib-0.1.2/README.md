# PyHTKLib

Python library for Hantek oscilloscope control and data acquisition, specifically designed for the Hantek6254BC model.

## Features

- Control Hantek6254BC oscilloscopes
- Data acquisition and processing
- Configuration management
- Measurement automation
- Data storage in CSV format
- Elasticsearch integration for data persistence

## Installation

1. Install the Hantek software:
   - Download from: https://www.hantek.com/uploadpic/hantek/files/20220517/Hantek-6000_Ver2.2.7_D2022032520220517110432.rar
   - Install the software following the provided instructions

2. Install PyHTKLib:
```bash
pip install PyHTKLib
```

## Usage

### Basic Usage

```python
from pyhtklib import Oscilloscope

# Initialize the oscilloscope
osc = Oscilloscope()

# Set up measurement configuration
osc.set_custom_config("measure.config.yaml")

# Initialize and start measurements
if osc.initialize():
    # Collect measurements
    batches = osc.collect_measurements(num_snapshots=10)
    
    # Process and save data
    success, bulk_id = osc.process_data(batches)
```

### Configuration

Create a YAML configuration file (e.g., `measure.config.yaml`):

```yaml
oscilloscope:
  # Channel 1 configuration
  ch1: 
    name: Custom Channel 1 Name
    probe-multiplier: 10
    volt-division: 8
    volts-per-division: 8
    channel-coupling: 0
    value-multiplier: 1.0
    off-voltage-threshold: 1.0
  
  # Channel 2 configuration 
  ch2: 
    name: Custom Channel 2 Name
    probe-multiplier: 1
    volt-division: 8
    volts-per-division: 8
    channel-coupling: 0
    value-multiplier: 4.0
  
  # General oscilloscope settings
  window: 7
  measurement-interval: 30
  n-snapshots: 2
  channel-mode: 4
  channels-enabled: [1, 1, 1, 1]
  channel-mask: 0x0F
  
  # Trigger settings
  trigger-channel: 0
  trigger-slope: 0
  trigger-mode: 0
  trigger-sweep: 0
  trigger-voltage: 0
  
  # Buffer settings
  buffer-length: 4096
  read-every-sample: 1
  yt-mode: 0

# Output directory for data files
export_dir: custom_outputs
```

### API Reference

#### Oscilloscope Class

```python
class Oscilloscope:
    def __init__(self):
        """Initialize the oscilloscope object."""
        
    def initialize(self) -> bool:
        """Initialize the oscilloscope hardware.
        Returns:
            bool: True if initialization was successful, False otherwise.
        """
        
    def set_custom_config(self, config_file_path: str) -> bool:
        """Load custom configuration from a YAML file.
        Args:
            config_file_path (str): Path to the configuration file.
        Returns:
            bool: True if configuration was loaded successfully.
        """
        
    def collect_measurements(self, num_snapshots: int) -> List[OscilloscopeData]:
        """Collect measurements from the oscilloscope.
        Args:
            num_snapshots (int): Number of snapshots to take.
        Returns:
            List[OscilloscopeData]: List of collected data batches.
        """
        
    def process_data(self, batches: List[OscilloscopeData]) -> Tuple[bool, Optional[str]]:
        """Process collected data and save to files/database.
        Args:
            batches (List[OscilloscopeData]): Data to process.
        Returns:
            Tuple[bool, Optional[str]]: Success status and bulk operation ID.
        """
```

#### Data Classes

```python
class OscilloscopeData:
    """Data class for storing oscilloscope measurements."""
    def __init__(self):
        """Initialize empty data structure for all channels."""
        self.ch1 = []
        self.ch2 = []
        self.ch3 = []
        self.ch4 = []
        
    def append_data_to_channel(self, ch: str, value: float):
        """Append a measurement value to a specific channel.
        Args:
            ch (str): Channel name (ch1, ch2, ch3, ch4).
            value (float): Measurement value to append.
        """
        
    def serialize_bulk_data_for_all_channels(self, bulk_id: str) -> List[Dict]:
        """Serialize data for bulk database insertion.
        Args:
            bulk_id (str): Unique identifier for the bulk operation.
        Returns:
            List[Dict]: Serialized data ready for database insertion.
        """
```

### Data Storage

The library supports two data storage methods:

1. CSV Files:
   - Data is stored in the configured output directory
   - Each channel's data is stored in a separate file
   - Files are organized by month and date
   - Format: `TIMESTAMP,RESOLUTION,CHANNEL,VALUE1,VALUE2,VALUE3...`

2. Elasticsearch (optional):
   - Configure in the YAML file
   - Supports bulk data insertion
   - Enables advanced querying and visualization

## Development

### Building the Package

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Hantek for providing the oscilloscope hardware and drivers
- Python community for the excellent tools and libraries

# Oscilloscope Data Collection 

## Overview
This project facilitates data collection from a Hantek6254BC oscilloscope using Python scripts. The codebase is organized in a modular manner, leveraging the Hantek SDK as the foundation for communication with the oscilloscope. Users can configure the oscilloscope settings, collect data, and retrieve the collected data for further analysis.
This project was inspired by similar projects on GitHub, where developers translated VB and C++ code provided by Hantek into Python for oscilloscope data collection. Leveraging this existing work, we have adapted and expanded the functionality to suit our specific requirements and preferences. Link to Github Project: https://github.com/CircuitAnalysis/Hantek/tree/main/6XXX%20USB%20Scope

The codebase is written in Python and structured into multiple files to ensure modularity and maintainability. We utilize the Hantek SDK for interfacing with the oscilloscope, enabling seamless communication between the Python scripts and the hardware device. The Hantek SDK provides a reliable and efficient way to interact with the oscilloscope, offering a wide range of functionalities and capabilities.

Users can easily run the main script (`main.py`) to initiate the data collection process. The project also includes separate files for handling oscilloscope configuration, data collection, and connection management. 

The Hantek SDK used in this project is available online and can be accessed for further reference or customization. 
Link to SDK .ddl file: https://github.com/CircuitAnalysis/Hantek/blob/main/6XXX%20USB%20Scope/Hantek%20Python%20API/Dll/x64/HTHardDll.dll
Link to SDK Manual: https://github.com/CircuitAnalysis/Hantek/blob/main/6XXX%20USB%20Scope/HT6004BX_SDK/Manual/SDK_HTHardDLL-EN.pdf
Link to documentation: https://github.com/CircuitAnalysis/Hantek/blob/main/6XXX%20USB%20Scope/Hantek%20Python%20API/Hantek%206000B(C%2CD%2CE)_Manual_English(V1.0.0).pdf

## Installation of Hantek Software
In order to view the waveforms captured by the oscilloscope, users will need to install the Hantek software specific to the Hantek6254BC model. This software provides a graphical user interface for visualizing waveforms and performing further analysis. Users can download the Hantek software from [Hantek's official website] Link: https://www.hantek.com/uploadpic/hantek/files/20220517/Hantek-6000_Ver2.2.7_D2022032520220517110432.rar, ensuring compatibility with the Hantek6254BC oscilloscope.

## Requirements
- Hantek6254BC oscilloscope
- Python 3.x
- Necessary libraries (details in the Installation section)

## Usage
1. **Run the Main Script:**
- Execute `main.py` to begin the data collection process. Ensure that the oscilloscope is connected and powered on before running the script.

2. **Using Custom Configuration Files:**
- You can provide your own configuration file with the `--config` parameter:
  ```
  python main.py --config your_custom_config.yaml
  ```
- This allows you to customize oscilloscope settings without modifying the original measure.config.yaml.
- Your custom config file must follow the same format as the default config file.
- A well-documented example configuration file is provided at `config/custom.config.example.yaml` to help you get started.

3. **Using Custom Database Settings:**
- **Command Line**: You can provide your own database configuration file with the `--db-config` parameter:
  ```
  python main.py --db-config config/database.config.example.json
  ```
- **Programmatic API**: You can also set database settings directly in your code:
  ```python
  from pqp_oscillo import Oscilloscope
  
  # Create oscilloscope instance
  osc = Oscilloscope()
  
  # Set custom database settings
  osc.set_database_settings({
      "url": "https://custom-elasticsearch:9200",
      "username": "custom_user",
      "password": "custom_password",
      "verify_ssl": True
  })
  
  # Continue with your measurements
  ```
- An example database configuration file is provided at `config/database.config.example.json`.
- Supported options include:
  - `url`: Elasticsearch server URL
  - `username` and `password`: Basic authentication credentials
  - `api_key`: API key for authentication
  - `use_api_key`: Whether to use API key instead of username/password
  - `timeout`: Connection timeout in seconds
  - `verify_ssl`: Whether to verify SSL certificates

## Data output
Collected data are stored inside `output\` folder. Data of very channel are stored to separate `.csv` file. The content of the csv file is following:
```
TIMESAMP,RESOLUTION,CHANNEL,VALUE1,VALUE2,VALUE3...

```
1. TIMESAMP - timestamp value with timezone info
2. RESOLUTION - x-axis resolution = number of measurements in one snapshot. This represent length of measured values array
3. CHANNEL - name of the channel
4. VALUE-N - measured values delimited by semicolon. Total number of measured values is represented in **RESOLUTION**

Every channel's csv file is appended for 30-mintues and afterwards all are moved to shared folder. If everything works fine without outage, new csv files for each channel are created every 30-minutes!

## Troubleshooting
- If you encounter any errors or issues during installation or usage, please refer to the troubleshooting section in the documentation or reach out to the project maintainers for assistance.

## Build
1. Create venv from `requirements.txt` and install all
2. Open cmd/terminal and activate venv
3. Run command:
    ```
    pyinstaller main.spec
    ```
4. This will create multiple folders. **Important is inside** `dist/` **folder**.
5. Check dist/ folder if it contains:
    - `measure.config.yaml` - configuration file for the application
    - `.env.enc` - ecrypted **.env** content using target machine's MAC address
    - `measure.exe` - you guessed it
7. Start mesure.exe

# pqp-oscillo

Python library for Hantek oscilloscope control and data acquisition.

## Installation

You can install the package using pip:

```bash
pip install pqp-oscillo
```

## Development

To install the package in development mode:

```bash
git clone https://github.com/yourusername/pqp-oscillo.git
cd pqp-oscillo
pip install -e .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Architecture and Workflow

The library is designed with a modular architecture to make it easy to customize and extend:

### Measurement Workflow
The measurement process follows these steps:
1. **Configuration Loading**: Loads measurement and database settings from files or code
2. **Device Initialization**: Finds and initializes the oscilloscope hardware
3. **Data Collection**: Takes snapshots from the oscilloscope
4. **Data Processing**: Saves data to files and sends to Elasticsearch

### Core Components
- **Oscilloscope Class**: Main interface for interacting with the hardware:
  ```python
  osc = Oscilloscope()
  osc.initialize()                      # Initialize hardware
  data = osc.collect_measurements(10)   # Take 10 snapshots
  osc.process_data(data)                # Process collected data
  ```

- **Configuration System**: Supports both command-line and programmatic configuration:
  ```python
  # From code:
  measurement_job(config_file="custom_config.yaml", db_config={"url": "https://custom-es:9200"})
  
  # From command line:
  python main.py --config custom_config.yaml --db-config database_config.json
  ```

## Environment Variables

The following environment variables need to be set for the library to work properly:

- `PYHTKLIB_API_KEY` - Your API key for authentication
- `PYHTKLIB_ES_USERNAME` - Elasticsearch username (defaults to "elastic" if not set)
- `PYHTKLIB_ES_PASSWORD` - Elasticsearch password

You can set these environment variables in your system or use a `.env` file in your project.

Example of setting environment variables in Windows:
```cmd
set PYHTKLIB_API_KEY=your_api_key_here
set PYHTKLIB_ES_USERNAME=your_username
set PYHTKLIB_ES_PASSWORD=your_password
```

Example of setting environment variables in Linux/macOS:
```bash
export PYHTKLIB_API_KEY=your_api_key_here
export PYHTKLIB_ES_USERNAME=your_username
export PYHTKLIB_ES_PASSWORD=your_password
```


