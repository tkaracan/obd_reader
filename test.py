import sqlite3
import time
from datetime import datetime
import obd
from commands import commands_list

# Initialize the database
def initialize_database():
    conn = sqlite3.connect('obd_readings.db')
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
    try_count = 0
    while True:
        if connection is None or not connection.is_connected():
            try:
                connection = obd.OBD()
            except Exception as e:
                time.sleep(2)  # Wait for 2 seconds before retrying
            print(f"{try_count} - Failed to connect to OBD-II interface")
            try_count += 1
    connection = obd.OBD()
    conn = sqlite3.connect('obd_readings.db')
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
                print(f"{command_name}: {response.value.magnitude}")
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

if __name__ == "__main__":
    initialize_database()
    collect_obd_data()