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
    # Try to establish an initial OBD connection
    while connection is None or not connection.is_connected():
        try:
            time.sleep(2)  # Ensure this sleep is before trying to connect
            connection = obd.OBD()
            print("Successfully connected to OBD-II interface.")
        except Exception as e:
            print(f"{try_count} - Failed to connect to OBD-II interface: {str(e)}")
            try_count += 1
            continue  # Keep trying until a connection is made

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

    # Continuously collect and store data
    while True:
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

        time.sleep(1)  # Pause before the next data collection cycle

if __name__ == "__main__":
    initialize_database()
    collect_obd_data()
