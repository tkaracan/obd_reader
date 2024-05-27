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
        value REAL
    )
    ''')
    conn.commit()
    conn.close()

# Collect data from OBD and write to SQLite database
def collect_obd_data():
    conn = sqlite3.connect('obd_data.db')
    cursor = conn.cursor()
    connection = obd.OBD()
    # Auto-connects to USB or RF port
    while True:
        for c in commands_list:  # Simplified command list
            command = c["Name"]
            response = connection.query(obd.commands[command])
            value = float(response.value.magnitude) if response.value else "N/A"
            cursor.execute('INSERT INTO car_data (timestamp, command, value) VALUES (?, ?, ?)',
                           (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), command, value))
        conn.commit()
        time.sleep(1)
    conn.close()

# Create GUI
def create_gui():
    root = tk.Tk()
    root.title("Car Data Display")
    root.geometry("800x500")
    root.config(bg='black')


    frames = {
        "RPM": tk.Label(root, text="", font=("Helvetica", 16), bg='black', fg='white'),
        "SPEED": tk.Label(root, text="", font=("Helvetica", 16), bg='black', fg='white'),
        "ENGINE_LOAD": tk.Label(root, text="", font=("Helvetica", 16), bg='black', fg='white')
    }

    for key, frame in frames.items():
        frame.pack(pady=20)

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
