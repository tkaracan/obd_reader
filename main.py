import threading
from datetime import time

from collect_data import OBDDataCollector
from db_reader import DbReader  # Assuming db_reader.py is set up with the DbReader class

def monitor_data():
    with DbReader('obd_readings.db') as db_reader:
        first_data = {
            'av_fuel_level': None,
            'last_mile': None
        }
        while True:
            if first_data['av_fuel_level'] is None:
                first_data['av_fuel_level'] = db_reader.get_average_of_last_n_entries("FUEL_LEVEL", 10)
            if first_data['last_mile'] is None:
                first_data['last_mile'] = db_reader.get_latest_entry("DISTANCE_SINCE_DTC_CLEAR")
            # Add more monitoring or logging features here as needed
            time.sleep(1)

if __name__ == "__main__":
    collector = OBDDataCollector()
    # Start OBD data collection in a separate thread
    obd_thread = threading.Thread(target=collector.collect_obd_data)
    obd_thread.start()

    # Start monitoring fuel levels in the main thread
    monitor_data()
