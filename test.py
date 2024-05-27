import threading
import sqlite3
import time
from datetime import datetime
import obd
from commands import commands_list
from speed import Speed
import tkinter as tk
from templates import frame_single


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
                time.sleep(2)  # Wait for 2 second before retrying

    connection = obd.OBD()
    while True:
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

def speed_update():
    speed_calculator = Speed()
    while True:
        average_speed = speed_calculator.Avspeed()
        if average_speed is not None:
            print(f"Average speed over the last 10 entries: {average_speed:.2f}")
        else:
            print("No speed entries found.")
        time.sleep(2)  # Wait for 2 seconds before the next retrieval

def create_gui(update_queue):
    w, h = 800, 500
    window_size = f"{w}x{h}"
    root = tk.Tk()
    root.title("Car Data Display")
    root.geometry(window_size)
    root.config(bg='black')
    column_count = 3
    frame_count = 9
    row_count = frame_count // column_count
    frame_width = (w - (column_count + 1) * 10) / column_count
    frame_height = (h - (row_count + 1) * 10) / row_count

    frames = []
    for i in range(frame_count):
        row = i // column_count
        col = i % column_count
        label = f"Label {i+1}"
        frame = frame_single(root, frame_width, frame_height, label, row, col)
        frames.append(frame)

    return frames, root



if __name__ == "__main__":
    initialize_database()
    create_gui()
    speed_update()
    obd_thread = threading.Thread(target=collect_obd_data, daemon=True)
    obd_thread.start()

