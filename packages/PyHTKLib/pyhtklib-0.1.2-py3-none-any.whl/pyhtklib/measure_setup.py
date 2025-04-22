from ctypes import windll, wintypes
from ctypes import Structure
import os

from .lib.dtos import DataStore


path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), r"dlls\x64\HTHardDll.dll"
)
OBJdll = windll.LoadLibrary(path)  # (64 bit)


class RELAYCONTROL(Structure):
    _fields_ = [
        ("bCHEnable", wintypes.BOOL * 4),
        ("nCHVoltDIV", wintypes.WORD * 4),
        ("nCHCoupling", wintypes.WORD * 4),
        ("bCHBWLimit", wintypes.BOOL * 4),
        ("nTrigSource", wintypes.WORD),
        ("bTrigFilt", wintypes.BOOL),
        ("nALT", wintypes.WORD),
    ]


class DATACONTROL(Structure):
    _fields_ = [
        (
            "nCHSet",
            wintypes.WORD,
        ),  # 0x0F in hexadecimal notation means all 4 channels are open
        ("nTimeDIV", wintypes.WORD),
        ("nTriggerSource", wintypes.WORD),  # Trigger source
        ("nHTriggerPos", wintypes.WORD),  # horizontal trigger position
        ("nVTriggerPos", wintypes.WORD),  # Vertical trigger position
        (
            "nTriggerSlope",
            wintypes.WORD,
        ),  # Use the rising edge as the trigger method
        ("nBufferLen", wintypes.ULONG),  # the length of the collected data
        ("nReadDataLen", wintypes.ULONG),  # the length of the read data
        (
            "nAlreadyReadLen",
            wintypes.ULONG,
        ),  # the length that has been read, only used in scan scrolling
        (
            "nALT",
            wintypes.WORD,
        ),  # Whether to trigger alternately. Note that alternate triggering is a software function
        ("nETSOpen", wintypes.WORD),
        ("nDriverCode", wintypes.WORD),  # drive number
        (
            "nLastAddress",
            wintypes.ULONG,
        ),  # record the last read end address of scan mode
        ("nFPGAVersion", wintypes.WORD),
    ]  # FPGA version number
    # ('nAddressOffset', wintypes.WORD) #Trigger jitter plus offset


VOLT_MULT = [0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10]
# VOLT_DIVISIONS = DataStore.volt_division #7.75
# VOLT_RESOLUTION = 256 #8 bit ADC

CH_ZERO_POS = [
    127,
    127,
    127,
    127,
]  # vertical zero position 0-255 [CH1, CH2, CH3, CH4]

# YTFormat = 2 # ! originally set to 0
collect = 1
nStartControl = 0
nStartControl = nStartControl + (
    1 if DataStore.oscillo.trigger_sweep == 0 else 0
)
nStartControl = nStartControl + (0 if DataStore.oscillo.yt_mode == 0 else 2)
nStartControl = nStartControl + (0 if collect == 1 else 4)

rcRelayControl = RELAYCONTROL()
stDataControl = DATACONTROL()

rcRelayControl.bCHEnable = (wintypes.BOOL * 4)(
    *DataStore.oscillo.channels_enabled
)
rcRelayControl.nCHVoltDIV = (wintypes.WORD * 4)(
    DataStore.oscillo.ch1.volts_per_division,
    DataStore.oscillo.ch2.volts_per_division,
    DataStore.oscillo.ch3.volts_per_division,
    DataStore.oscillo.ch4.volts_per_division,
)
rcRelayControl.nCHCoupling = (wintypes.WORD * 4)(
    DataStore.oscillo.ch1.channel_coupling,
    DataStore.oscillo.ch2.channel_coupling,
    DataStore.oscillo.ch3.channel_coupling,
    DataStore.oscillo.ch4.channel_coupling,
)  # Design coupling mode DC=0, AC=1
rcRelayControl.bCHBWLimit = (wintypes.BOOL * 4)(
    0, 0, 0, 0
)  # Whether to enable 20M filtering
rcRelayControl.nTrigSource = DataStore.oscillo.trigger_channel  # Trigger source
rcRelayControl.bTrigFilt = 0  # Whether to enable 20M filtering
rcRelayControl.nALT = 0  # Whether to trigger alternately. Note that alternate triggering is a software function

stDataControl.nCHSet = (
    DataStore.oscillo.channel_mask
)  # 0x0F (15) means all 4 channels are open
stDataControl.nTimeDIV = (
    DataStore.oscillo.measurement_window
)  # Time base index value
stDataControl.nTriggerSource = (
    DataStore.oscillo.trigger_channel
)  # Trigger source
stDataControl.nHTriggerPos = 50  # horizontal trigger position
stDataControl.nVTriggerPos = (
    DataStore.oscillo.trigger_voltage
)  # Vertical trigger position
stDataControl.nTriggerSlope = (
    DataStore.oscillo.trigger_slope
)  # Use the rising edge as the trigger method
stDataControl.nBufferLen = (
    DataStore.oscillo.buffer_length
)  # the length of the collected data
stDataControl.nReadDataLen = (
    DataStore.oscillo.buffer_length
)  # the length of the read data
stDataControl.nAlreadyReadLen = (
    0  # the length that has been read, only used in scan scrolling
)
stDataControl.nALT = 0  # Whether to trigger alternately. Note that alternate triggering is a software function
