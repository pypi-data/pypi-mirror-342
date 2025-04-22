from ..lib.constants import GET_ES_OSICLLO_DATA_INDEX
from ..lib.dtos import DataStore
import logging
from datetime import datetime


class OscilloscopeData:
    def __init__(self) -> None:
        # self._timestamp = None # dt.now(timezone.utc)
        self.ch1 = []
        self.ch2 = []
        self.ch3 = []
        self.ch4 = []

    def append_data_to_channel(self, ch: str, value: float):
        ch_values = getattr(self, ch, None)
        # if ch_values is None: return
        ch_values.append(value)

    def serialize_bulk_data_for_all_channels(self, bulk_id: str):
        channels_voltages = {
            ch: getattr(self, ch) for ch in DataStore.oscillo.channels
        }
        bulk_data = []
        for ch, voltages in channels_voltages.items():
            channel_name = DataStore.oscillo.channel_name(ch)
            bulk_data.append(
                {
                    "_op_type": "create",
                    "_index": GET_ES_OSICLLO_DATA_INDEX(ch),
                    "_source": {
                        "channel": ch,
                        "channel_alias": channel_name,
                        "timestamp_start_measurement": DataStore.timestamp_start_mesurement_task,
                        "timestamp_read_measurement": DataStore.timestamp_read_measurement_data,
                        # "timestamp_bulk": DataStore.timestamp_bulk,  # if multiple snapshots, this timestamp is same for all
                        "bulk_id": bulk_id,  # measurement_id is to identify measurements run in same measurement cycle, meaning if every 10 seconds we do 4 measurements, so those 4 will have same measurement id
                        "voltage": voltages,
                        "bulk_interval": DataStore.oscillo.measurement_interval,
                        "n_snapshots": DataStore.oscillo.n_snapshots,
                    },
                }
            )
        return bulk_data