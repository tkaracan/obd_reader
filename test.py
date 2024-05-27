import threading
import sqlite3
import time
from datetime import datetime
import obd
from commands import commands_list
from speed import Speed


# Initialize the database
def initialize_database():
    conn = sqlite3.connect('obd_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS car_data (
            timestamp TEXT,
            command TEXT,
            value TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Collect data from OBD and write to SQLite database
def collect_obd_data():
    connection = None
    while True:
        if connection is None or not connection.is_connected():
            try:
                connection = obd.OBD()
            except Exception as e:
                print(f"Failed to connect to OBD-II interface: {str(e)}")
                time.sleep(1)  # Wait for 1 second before retrying
                continue

        conn = sqlite3.connect('obd_data.db')
        cursor = conn.cursor()

        # Check which commands are supported once
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

        # Auto-connects to USB or RF port
        for command_name in supported_commands:
            response = connection.query(obd.commands[command_name])
            if response.value is not None:
                if hasattr(response.value, 'magnitude'):
                    value = response.value.magnitude
                else:
                    value = str(response.value)
            else:
                value = "N/A"
            cursor.execute('INSERT INTO car_data (timestamp, command, value) VALUES (?, ?, ?)',
                           (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), command_name, value))
            conn.commit()
        conn.close()
        time.sleep(1)  # Wait for 1 second before the next iteration


# Function to retrieve average speed data every 2 seconds
def get_average_speed():
    speed_calculator = Speed()
    while True:
        average_speed = speed_calculator.Avspeed()
        if average_speed is not None:
            print(f"Average speed over the last 10 entries: {average_speed:.2f}")
        else:
            print("No speed entries found.")
        time.sleep(2)  # Wait for 2 seconds before the next retrieval


if __name__ == "__main__":
    initialize_database()
    obd_thread = threading.Thread(target=collect_obd_data, daemon=True)
    speed_thread = threading.Thread(target=get_average_speed, daemon=True)
    obd_thread.start()
    speed_thread.start()

    while True:
        # Keep the main thread running
        time.sleep(1)