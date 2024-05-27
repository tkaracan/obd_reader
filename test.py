import tkinter as tk
import threading
import sqlite3
import time
from datetime import datetime
import obd
from commands import commands_list

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
    connection = obd.OBD()

    if not connection.is_connected():
        print("Failed to connect to OBD-II interface.")
        return

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
    while True:
        for command_name in supported_commands:
            response = connection.query(obd.commands[command_name])
            if response.value is not None:
                if hasattr(response.value, 'magnitude'):
                    value = str(response.value.magnitude)
                else:
                    value = str(response.value)
            else:
                value = "N/A"
            cursor.execute('INSERT INTO car_data (timestamp, command, value) VALUES (?, ?, ?)',
                           (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), command_name, value))
        conn.commit()
        time.sleep(1)
    conn.close()

# Define frame styles
def define_styles(root):
    styles = {
        "single_data": {"font": ("Helvetica", 16), "bg": "black", "fg": "white"},
        # Add more styles here if needed
    }
    return styles

# Create GUI
def create_gui():
    w, h = 800, 500
    window_size = f"{w}x{h}"
    root = tk.Tk()
    root.title("Car Data Display")
    root.geometry(window_size)
    root.config(bg='black')

    # Define frame configurations
    frame_configs = [
        {"id": 1, "title": "RPM", "style": "single_data", "row": 0, "column": 0},
        {"id": 2, "title": "SPEED", "style": "single_data", "row": 0, "column": 1},
        {"id": 3, "title": "ENGINE_LOAD", "style": "single_data", "row": 1, "column": 0}
    ]

    # Define styles
    styles = define_styles(root)

    # Create frames based on configurations
    frames = {}
    for config in frame_configs:
        style = styles[config["style"]]
        frame = tk.Label(root, text=config["title"], font=style["font"], bg=style["bg"], fg=style["fg"])
        frame.grid(row=config["row"], column=config["column"], padx=20, pady=20)
        frames[config["title"]] = frame

    # Start the thread to update GUI labels
    threading.Thread(target=update_labels, args=(frames,), daemon=True).start()
    root.mainloop()

# Update GUI labels from database
def update_labels(frames):
    conn = sqlite3.connect('obd_data.db')
    cursor = conn.cursor()
    while True:
        cursor.execute('SELECT command, value FROM car_data ORDER BY timestamp DESC LIMIT 10')
        rows = cursor.fetchall()
        for command, value in rows:
            if command in frames:
                frames[command].config(text=f"{command}: {value}")
        time.sleep(1)  # Refresh every second

if __name__ == "__main__":
    initialize_database()
    threading.Thread(target=collect_obd_data, daemon=True).start()
    create_gui()
