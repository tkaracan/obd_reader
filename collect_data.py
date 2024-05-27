import sqlite3
import time
from datetime import datetime
import obd
from commands import commands_list

class OBDDataCollector:
    def __init__(self, db_path='obd_readings.db'):
        self.db_path = db_path
        self.initialize_database()

    def initialize_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS car_data (
                    timestamp TEXT,
                    command TEXT,
                    value TEXT
                )
            ''')
            conn.commit()

    def collect_obd_data(self):
        connection = None
        try_count = 0
        while connection is None or not connection.is_connected():
            try:
                time.sleep(2)
                connection = obd.OBD()
                print("Successfully connected to OBD-II interface.")
            except Exception as e:
                print(f"{try_count} - Failed to connect to OBD-II interface: {str(e)}")
                try_count += 1
                continue

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        supported_commands = []
        for c in commands_list:
            command_name = c["Name"]
            try:
                command = obd.commands[command_name]
                response = connection.query(command)
                if not response.is_null():
                    supported_commands.append(command_name)
            except KeyError:
                print(f"Command {command_name} is not supported")

        while True:
            for command_name in supported_commands:
                response = connection.query(obd.commands[command_name])
                value = str(response.value.magnitude) if hasattr(response.value, 'magnitude') else str(response.value)
                cursor.execute('INSERT INTO car_data (timestamp, command, value) VALUES (?, ?, ?)',
                               (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), command_name, value))
                conn.commit()
            time.sleep(1)
