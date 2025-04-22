## Main class which will communicate with osciloscope

from ctypes import POINTER, wintypes
import time
from typing import List, Dict, Any, Tuple, Optional
from venv import logger
import warnings
import urllib3


# Suppress InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Suppress all warnings from elasticsearch
warnings.filterwarnings("ignore", module="elasticsearch")


from datetime import datetime as dt

# Internal imports using relative paths
from ..database.es import _bulk_measured_data, test_connection, set_database_settings
from ..lib.dtos import DataStore
from ..lib.snapshot import _create_snapshot, _read_data_from_snapshot
from ..lib.tasks import _write_data_to_output_files
from ..measure_setup import (
    DATACONTROL,
    RELAYCONTROL,
    OBJdll,
    rcRelayControl,
    stDataControl,
)
from .data import OscilloscopeData
from ..lib.constants import API_KEY, ES_PASSWORD, ES_USERNAME

class Oscilloscope:
    def __init__(self):
        logger.info("Oscilloscope object created")
        
        # Default database settings - simplified
        self._es_settings = {
            "url": "https://localhost:9200",
            "username": ES_USERNAME,
            "password": ES_PASSWORD,
            "timeout": 300
        }
        
        # Initialize device index
        self.device_index = 0  # Default to first device
        
    def set_custom_config(self, config_file_path):
        """
        Allows users to set a custom configuration file for measurements.
        
        Args:
            config_file_path (str): Path to the YAML configuration file.
            
        Returns:
            bool: True if configuration was successfully loaded, False otherwise.
        """
        try:
            import yaml
            from ..lib.dtos import DataStore
            
            # Load the custom configuration file
            logger.info(f"Loading custom configuration from {config_file_path}")
            with open(config_file_path, mode="r", encoding="utf-8") as file:
                app_config = yaml.safe_load(file.read())
            
            if not app_config:
                logger.error("Failed to load configuration or file is empty")
                return False
                
            # Update the DataStore with the new configuration
            success = DataStore.update_config(app_config)
            if success:
                logger.info("Custom configuration successfully loaded")
            else:
                logger.error("Failed to update configuration")
                
            return success
        except Exception as e:
            logger.error(f"Error loading custom configuration: {str(e)}")
            return False
        
    def set_database_settings(self, settings: Dict[str, Any]) -> bool:
        """
        Configure custom database settings for sending measurement data.
        
        Args:
            settings (dict): Dictionary containing database connection settings.
                Possible keys:
                - url: Elasticsearch server URL (default: "https://localhost:9200")
                - username: Username for authentication
                - password: Password for authentication
                - timeout: Connection timeout in seconds (default: 300)
                
        Returns:
            bool: True if settings were successfully updated
        """
        try:
            logger.info("Updating database settings...")
            
            if not settings:
                logger.warning("Empty database settings provided. Using defaults.")
                return False
                
            # Update settings
            if settings.get("url"):
                self._es_settings["url"] = settings["url"]
                
            if settings.get("username"):
                self._es_settings["username"] = settings["username"]
                
            if settings.get("password"):
                self._es_settings["password"] = settings["password"]
                
            if settings.get("timeout"):
                self._es_settings["timeout"] = settings["timeout"]
            
            logger.info(f"Database settings successfully updated. URL: {self._es_settings['url']}")
            return True
        except Exception as e:
            logger.error(f"Error updating database settings: {str(e)}")
            return False
        
    def get_database_settings(self) -> Dict[str, Any]:
        """
        Get the current database settings.
        
        Returns:
            dict: Dictionary containing the current database settings
        """
        return self._es_settings.copy()
        
    def validate_database_settings(self) -> bool:
        """
        Validate that the current database settings are properly configured.
        
        Returns:
            bool: True if settings are valid, False otherwise
        """
        try:
            # Check if URL is set and valid
            if not self._es_settings.get("url"):
                logger.error("Database URL is not set")
                return False
                
            # Check if authentication is properly configured
            if not self._es_settings.get("username") or not self._es_settings.get("password"):
                logger.error("Username or password is missing")
                return False
            
            # Test connection to Elasticsearch
            try:
                from elasticsearch import Elasticsearch
                
                es = Elasticsearch(
                    self._es_settings["url"],
                    http_auth=(self._es_settings["username"], self._es_settings["password"]),
                    timeout=10  # Short timeout for testing
                )
                
                if es.ping():
                    logger.info("Successfully validated database connection")
                    return True
                else:
                    logger.warning("Could not connect to Elasticsearch server. Check connection settings.")
                    return False
            except Exception as e:
                logger.warning(f"Could not test Elasticsearch connection: {str(e)}")
                # Don't fail on connection test, just log warning
                return True
                
        except Exception as e:
            logger.error(f"Error validating database settings: {str(e)}")
            return False
        
    def init_devices(self):
        dsoInitHard = OBJdll.dsoInitHard
        dsoInitHard.argtypes = [wintypes.WORD]
        dsoInitHard.restype = wintypes.WORD
        logger.info("Init: dsoInitHard")
        DataStore.oscillo.init_ok = dsoInitHard(DataStore.oscillo.device_index)
        logger.info("✔")

        ################################################
        #     INITIALIZE FUNCTION GENERATOR (DDS)
        ################################################

        # ddsSetCmd = OBJdll.ddsSetCmd
        # ddsSetCmd.argtypes = [wintypes.WORD, wintypes.USHORT]
        # ddsSetCmd.restype = wintypes.ULONG
        # DataStore.oscillo.ready_and_ok = ddsSetCmd(DataStore.oscillo.device_index, WAVE_MODE)
        # logger.info(f"ddsSetCmd={DataStore.oscillo.ready_and_ok}")

        # ddsSDKSetWaveType = OBJdll.ddsSDKSetWaveType
        # ddsSDKSetWaveType.argtypes = [wintypes.WORD, wintypes.WORD]
        # ddsSDKSetWaveType.restype = wintypes.WORD
        # DataStore.oscillo.ready_and_ok = ddsSDKSetWaveType(DataStore.oscillo.device_index, WAVE_TYPE)
        # logger.info(f"ddsSDKSetWaveType={DataStore.oscillo.ready_and_ok}")

        # ddsSDKSetFre = OBJdll.ddsSDKSetFre
        # ddsSDKSetFre.argtypes = [wintypes.WORD, wintypes.FLOAT]
        # ddsSDKSetFre.restype = wintypes.FLOAT
        # DataStore.oscillo.ready_and_ok = ddsSDKSetFre(DataStore.oscillo.device_index, FREQUENCY)
        # logger.info(f"ddsSDKSetFre={DataStore.oscillo.ready_and_ok}")

        # ddsSDKSetAmp = OBJdll.ddsSDKSetAmp
        # ddsSDKSetAmp.argtypes = [wintypes.WORD, wintypes.WORD]
        # ddsSDKSetAmp.restype = wintypes.WORD
        # DataStore.oscillo.ready_and_ok = ddsSDKSetAmp(DataStore.oscillo.device_index, AMPLITUDE)
        # logger.info(f"ddsSDKSetAmp={DataStore.oscillo.ready_and_ok}")

        # ddsSDKSetOffset = OBJdll.ddsSDKSetOffset
        # ddsSDKSetOffset.argtypes = [wintypes.WORD, wintypes.SHORT]
        # ddsSDKSetOffset.restype = wintypes.SHORT
        # DataStore.oscillo.ready_and_ok = ddsSDKSetOffset(DataStore.oscillo.device_index, OFFSET)
        # logger.info(f"ddsSDKSetOffset={DataStore.oscillo.ready_and_ok}")

        # ddsSetOnOff = OBJdll.ddsSetOnOff
        # ddsSetOnOff.argtypes = [wintypes.WORD, wintypes.SHORT]
        # ddsSetOnOff.restype = wintypes.ULONG
        # DataStore.oscillo.ready_and_ok = ddsSetOnOff(DataStore.oscillo.device_index, 1)
        # logger.info(f"ddsSetOnOff={DataStore.oscillo.ready_and_ok}")

        # logger.info("Completed DDS Configuration")

        ################################################
        #         INITIALIZE OSCILLOSCOPE (DSO)
        ################################################

        dsoHTADCCHModGain = OBJdll.dsoHTADCCHModGain
        dsoHTADCCHModGain.argtypes = [wintypes.WORD, wintypes.WORD]
        dsoHTADCCHModGain.restype = wintypes.WORD
        logger.info("Init: dsoHTADCCHModGain")
        DataStore.oscillo.init_ok = dsoHTADCCHModGain(
            DataStore.oscillo.device_index, 4
        )  # Set the analog amplitude correction
        logger.info("✔")

        dsoHTSetSampleRate = OBJdll.dsoHTSetSampleRate
        dsoHTSetSampleRate.argtypes = [
            wintypes.WORD,
            wintypes.WORD,
            POINTER(RELAYCONTROL),
            POINTER(DATACONTROL),
        ]
        dsoHTSetSampleRate.restype = wintypes.WORD
        logger.info("Init: dsoHTSetSampleRate")
        DataStore.oscillo.init_ok = dsoHTSetSampleRate(
            DataStore.oscillo.device_index,
            DataStore.oscillo.yt_mode,
            rcRelayControl,
            stDataControl,
        )  # Set the sample rate
        logger.info("✔")

        dsoHTSetCHAndTrigger = OBJdll.dsoHTSetCHAndTrigger
        dsoHTSetCHAndTrigger.argtypes = [
            wintypes.WORD,
            POINTER(RELAYCONTROL),
            wintypes.WORD,
        ]
        dsoHTSetCHAndTrigger.restype = wintypes.WORD
        logger.info("Init: dsoHTSetCHAndTrigger")
        DataStore.oscillo.init_ok = dsoHTSetCHAndTrigger(
            DataStore.oscillo.device_index, rcRelayControl, stDataControl.nTimeDIV
        )  # Set the channel switch and voltage level
        logger.info("✔")

        dsoHTSetRamAndTrigerControl = OBJdll.dsoHTSetRamAndTrigerControl
        dsoHTSetRamAndTrigerControl.argtypes = [
            wintypes.WORD,
            wintypes.WORD,
            wintypes.WORD,
            wintypes.WORD,
            wintypes.WORD,
        ]
        dsoHTSetRamAndTrigerControl.restype = wintypes.WORD
        logger.info("Init: dsoHTSetRamAndTrigerControl")
        DataStore.oscillo.init_ok = dsoHTSetRamAndTrigerControl(
            DataStore.oscillo.device_index,
            stDataControl.nTimeDIV,
            stDataControl.nCHSet,
            stDataControl.nTriggerSource,
            0,
        )  # Set the trigger source
        logger.info("✔")

        for i in range(4):
            dsoHTSetCHPos = OBJdll.dsoHTSetCHPos
            dsoHTSetCHPos.argtypes = [
                wintypes.WORD,
                wintypes.WORD,
                wintypes.WORD,
                wintypes.WORD,
                wintypes.WORD,
            ]
            dsoHTSetCHPos.restype = wintypes.WORD
            logger.info(f"Init: dsoHTSetCHPos CH={i+1}")
            DataStore.oscillo.init_ok = dsoHTSetCHPos(
                DataStore.oscillo.device_index,
                rcRelayControl.nCHVoltDIV[i],
                128,
                i,
                DataStore.oscillo.adc_channel_mode,
            )  # Set the vertical position of the channel
            logger.info("✔")
            # logger.info(f"rcRelayControl.nCHVoltDIV[i]={rcRelayControl.nCHVoltDIV[i]}")

        dsoHTSetVTriggerLevel = OBJdll.dsoHTSetVTriggerLevel
        dsoHTSetVTriggerLevel.argtypes = [
            wintypes.WORD,
            wintypes.WORD,
            wintypes.WORD,
        ]
        dsoHTSetVTriggerLevel.restype = wintypes.WORD
        logger.info("Init: dsoHTSetVTriggerLevel")
        DataStore.oscillo.init_ok = dsoHTSetVTriggerLevel(
            DataStore.oscillo.device_index, stDataControl.nVTriggerPos, 4
        )  # Set the trigger vertical position to be the same as channel 1
        logger.info("✔")

        dsoHTSetTrigerMode = OBJdll.dsoHTSetTrigerMode
        dsoHTSetTrigerMode.argtypes = [
            wintypes.WORD,
            wintypes.WORD,
            wintypes.WORD,
            wintypes.WORD,
        ]
        dsoHTSetTrigerMode.restype = wintypes.WORD
        logger.info("Init: dsoHTSetTrigerMode")
        DataStore.oscillo.init_ok = dsoHTSetTrigerMode(
            DataStore.oscillo.device_index,
            DataStore.oscillo.trigger_mode,
            stDataControl.nTriggerSlope,
            0,
        )
        logger.info("✔")
        return

        # logger.info("Initialization with oscilloscope...")
        # self.device_index = 0
        # dsoInitHard = OBJdll.dsoInitHard
        # dsoInitHard.argtypes = [wintypes.WORD]
        # dsoInitHard.restype = wintypes.WORD
        # logger.info(" Init: dsoInitHard")
        # self.init_ok = dsoInitHard(self.device_index)
        # # DataStore.oscillo.init_ok = dsoInitHard(DataStore.oscillo.device_index)
        # if self.init_ok:
        #     logger.info("✔ Initialization successful")
        # else:
        #     logger.error("❌ Initialization failed")


    def find_devices(self) -> bool:
        """Searches for the oscilloscope device and verifies connection."""
        deviceArray = (wintypes.WORD * 32)()  # Array to hold device indices
        dsoHTSearchDevice = OBJdll.dsoHTSearchDevice
        dsoHTSearchDevice.argtypes = [POINTER(wintypes.WORD)]  # Argument type (pointer to WORD)
        dsoHTSearchDevice.restype = wintypes.WORD  # Return type (WORD)
        
        logger.info("Searching for connected oscilloscope devices...")
        
        # Call the device search function
        result = dsoHTSearchDevice(deviceArray)
        
        if result == 0:  # No devices found
            logger.error("No oscilloscope found.")
            return False  # No device found
        
        # Iterate through the deviceArray and find the first device
        for i in range(32):
            if deviceArray[i] != 0:  # Non-zero means the device is present at this index
                DataStore.oscillo.device_index = i  # Set the device index to the found device's index
                logger.info(f"Found device at index {DataStore.oscillo.device_index}")
                return True  # Device found, exit and return True
        
        logger.error("No oscilloscope found after checking all devices.")
        return False  # Return False if no device found after checking all


    def connect(self) -> bool:
        logger.info("Connecting...")

        # Search for oscilloscope
        if not self.find_devices():
            logger.error("Did not find any device.")
            return False

        dsoHTDeviceConnect = OBJdll.dsoHTDeviceConnect
        dsoHTDeviceConnect.argtypes = [wintypes.WORD]
        dsoHTDeviceConnect.restype = wintypes.WORD

        # Try connecting
        connection_status = dsoHTDeviceConnect(self.device_index)
        if connection_status == 1:
            logger.info(f"Osciloskop sucsessfully connected at index {self.device_index}.")
            return True
        else:
            logger.error("Connection faild")
            return False


    def get_device_info(self) -> dict:
        """Returns basic information about the oscilloscope (model, firmware version, etc.)."""
        device_info = {}

        # Check if a device is connected
        if self.device_index == -1:
            logger.error("No device connected. Please search for the device first.")
            return device_info  # Return empty dict if no device is found

        # Retrieve the FPGA version
        try:
            fpga_version = OBJdll.dsoGetFPGAVersion(self.device_index)
            device_info['FPGA Version'] = fpga_version
            logger.info(f"FPGA Version: {fpga_version}")
        except Exception as e:
            logger.error(f"Error retrieving FPGA version: {e}")
        
        return device_info


    def start_data_collection(self, start_control: int) -> bool:
        logger.info("Starts data collection from the oscilloscope..")
        if not self.find_devices():
            logger.error("No device connected. Please search for the device first.")
            return False  # Return False if no device is found

        try:
            # Ensure the device is initialized before starting data collection
            dsoHTStartCollectData = OBJdll.dsoHTStartCollectData
            dsoHTStartCollectData.argtypes = [wintypes.WORD, wintypes.WORD]
            dsoHTStartCollectData.restype = wintypes.WORD

            logger.info(f"Starting data collection on device {self.device_index}...")
            """
            0: AUTO Trigger - Starts the data collection when the oscilloscope triggers automatically.

            1: ROLL Mode - The oscilloscope collects data continuously in roll mode.

            2: Stop after collection - Starts data collection and stops automatically after capturing data.
            """
            # Start data collection by calling the function with the appropriate control parameter
            result = dsoHTStartCollectData(self.device_index, start_control)

            
            if result != 0:
                logger.info("✔ Data collection started successfully.")
                print(result)
                return True  # Success
            else:
                logger.error("❌ Failed to start data collection.")
                return False  # Failure
        except Exception as e:
            logger.error(f"Error while starting data collection: {e}")
            return False  # Return False if an error occurs


    def measure(self, i_snapshot: int):
        _create_snapshot(i_snapshot)
        return _read_data_from_snapshot(i_snapshot)
    

    def write_data_to_output_files(self, batches: List[OscilloscopeData]):
        return _write_data_to_output_files(batches)
    
    
    def bulk_measured_data(self, data: List[OscilloscopeData]) -> Tuple[bool, Optional[str]]:
        """
        Send measured data to Elasticsearch using bulk operations.
        
        Args:
            data (List[OscilloscopeData]): List of oscilloscope data to send
            
        Returns:
            tuple: (success, bulk_id) - Whether the operation was successful and the bulk ID
        """
        try:
            from elasticsearch import Elasticsearch
            from elasticsearch.helpers import bulk
            import uuid
            
            # Create Elasticsearch client with simplified settings
            es = Elasticsearch(
                self._es_settings["url"],
                http_auth=(self._es_settings["username"], self._es_settings["password"]),
                timeout=self._es_settings["timeout"]
            )

            if not data:
                logger.warning("No data to send.")
                return False, None

            bulk_data = []
            bulk_id = str(uuid.uuid4())

            for batch in data:
                bulk_data.extend(batch.serialize_bulk_data_for_all_channels(bulk_id))

            try:
                success, failed = bulk(es, bulk_data)

                if success:
                    logger.info(f"✔ Bulk data sent to ES (bulk_id={bulk_id})")
                    return True, bulk_id
                else:
                    logger.error(f"❌ Error sending bulk data: {failed}")
                    return False, bulk_id
            except Exception as e:
                logger.error(f"❌ Error during bulk operation: {str(e)}")
                return False, None
        except Exception as e:
            logger.error(f"Error in bulk_measured_data: {str(e)}")
            return False, None

    def initialize(self) -> bool:
        """
        Initialize the oscilloscope by finding and setting up devices.
        
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        try:
            logger.info("Initialization of oscilloscope...")
            if not self.find_devices():
                logger.error("No oscilloscope device found.")
                return False
                
            self.init_devices()
            return True
        except Exception as e:
            logger.error(f"Error initializing oscilloscope: {str(e)}")
            return False
    
    def collect_measurements(self, num_snapshots: int) -> List[OscilloscopeData]:
        """
        Collect measurements from the oscilloscope.
        
        Args:
            num_snapshots: Number of snapshots to take
            
        Returns:
            List[OscilloscopeData]: List of collected data batches
        """
        batches = []
        try:
            for i in range(1, num_snapshots + 1):
                batch = self.measure(i)  # measure data from oscilloscope
                batches.append(batch)
                
            if not batches:
                logger.error("Empty batches!")
            
            return batches
        except Exception as e:
            logger.error(f"Error collecting measurements: {str(e)}")
            return batches
    
    def process_data(self, batches: List[OscilloscopeData]) -> Tuple[bool, Optional[str]]:
        """
        Process collected data - write to files and send to database.
        
        Args:
            batches: List of data batches to process
            
        Returns:
            Tuple[bool, Optional[str]]: Success status and bulk operation ID
        """
        try:
            if not batches:
                logger.error("No data to process!")
                return False, None
                
            # Write data to output files
            self.write_data_to_output_files(batches)
            
            # Send data to Elasticsearch
            success, bulk_id = self.bulk_measured_data(batches)
                
            return success, bulk_id
        except Exception as e:
            logger.error(f"Error processing data: {str(e)}")
            return False, None