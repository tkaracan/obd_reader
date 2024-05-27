import tkinter as tk
import threading
import queue
import time
from datetime import datetime
from commands import commands_list

import obd
import csv
import random
from data_calculations import dict_test, calculate_distance, kmh_to_mph, celsius_to_fahrenheit, percent, rpm_to_rpm, \
    fuel_level_to_percent, calculate_mpg

first_values = {}


def create_gui(update_queue):
    w, h = 800, 500
    window_size = f"{w}x{h}"
    root = tk.Tk()
    root.title("Car Data Display")
    root.geometry(window_size)
    root.config(bg='black')

    keys = {
        "ENGINE_LOAD": "Engine Load (%)",
        "DISTANCE_SINCE_DTC_CLEAR": "Distance (km)",
        "RPM": "RPM",
        "SPEED": "Speed (mph)",
        "FUEL_LEVEL": "Fuel Level (%)",
        "AMBIANT_AIR_TEMP": "Inside Temp (°F)",
        "THROTTLE_POS_B": "Throttle Position - B",
        "ACCELERATOR_POS_D": "Accelerator Position - D",
        "ACCELERATOR_POS_E": "Accelerator Position - E",
    }

    frames = {key: create_frame(root, label, index, keys) for index, (key, label) in enumerate(keys.items())}

    def update_labels():
        while True:
            all_data = update_queue.get()
            for key, value in all_data.items():
                update_frame(frames[key], keys[key], value['id'], value['data'])
            update_queue.task_done()

    thread_update = threading.Thread(target=update_labels, daemon=True)
    thread_update.start()
    root.mainloop()


def create_frame(root, label, index, keys):
    num_columns = 3
    padding = 10
    w, h = 800, 500
    frame_width = int((w - (num_columns * 2) * padding) / num_columns)
    frame_height = int((h - (len(keys) + num_columns - 1) // num_columns * 2 * padding) / (
                (len(keys) + num_columns - 1) // num_columns))

    frame = tk.Frame(root, height=frame_height, width=frame_width, bg='black', highlightbackground='white',
                     highlightthickness=1)
    row, col = divmod(index, num_columns)
    frame.grid(row=row, column=col, padx=padding, pady=padding, sticky="nsew")
    frame.grid_propagate(False)

    # Store the dimensions as attributes of the frame
    frame.frame_width = frame_width
    frame.frame_height = frame_height

    return frame


def update_frame(frame, label, frame_id, value):
    if not hasattr(frame, 'initialized') or not frame.initialized:
        # Clear previous widgets if frame is not initialized
        for widget in frame.winfo_children():
            widget.destroy()

        if frame_id == "dictionary":
            frame.initialized = True
            frame.widgets = []
            y_offset = 25  # Start placing at 25 px vertically
            for subkey, subvalue in value.items():
                key_label = tk.Label(frame, text=f"{subkey}", font=("Noto Sans Mono", 10), bg='black', fg='white')
                key_label.place(x=20, y=y_offset, anchor='w')
                # Format subvalue for display
                formatted_subvalue = f"{subvalue:.1f}" if isinstance(subvalue, (int, float)) else str(subvalue)
                value_label = tk.Label(frame, text=formatted_subvalue, font=("Noto Sans Mono", 11), bg='black',
                                       fg='white')
                value_label.place(x=frame.frame_width - 20, y=y_offset, anchor='e')
                frame.widgets.append((key_label, value_label))
                y_offset += 30  # Move the next pair down by 30 px

        elif frame_id == "single":
            frame.initialized = True
            frame.key_label = tk.Label(frame, text=label, font=("Noto Sans Mono", 10), bg='black', fg='white',
                                       anchor='nw')
            frame.key_label.place(x=10, y=10)
            frame.value_label = tk.Label(frame, text="", font=("Noto Sans Mono", 20), bg='black', fg='white')
            frame.value_label.place(relx=0.5, rely=0.5, anchor='center')

        elif frame_id == "percent":
            frame.initialized = True
            # Handle percent frame
            frame.key_label = tk.Label(frame, text=label, font=("Noto Sans Mono", 10), bg='black', fg='white',
                                       anchor='nw')
            frame.key_label.place(x=10, y=10)

            # Create the percentage box
            frame.percent_box = tk.Frame(frame, bg='white', height=frame.frame_height - 90, width=0)
            frame.percent_box.place(relx=0, rely=0.5, anchor='w')

            frame.value_label = tk.Label(frame, text="", font=("Noto Sans Mono", 20), bg='black', fg='white')
            frame.value_label.place(relx=0.5, rely=0.5, anchor='center')

    if frame_id == "dictionary":
        # Update dictionary frame
        if not isinstance(value, dict):
            value = {"Current Level": value}

        y_offset = 25  # Start placing at 25 px vertically
        for widget in frame.winfo_children():
            widget.destroy()
        frame.widgets = []
        for subkey, subvalue in value.items():
            key_label = tk.Label(frame, text=f"{subkey}", font=("Noto Sans Mono", 10), bg='black', fg='white')
            key_label.place(x=20, y=y_offset, anchor='w')
            # Format subvalue for display
            formatted_subvalue = f"{subvalue:.1f}" if isinstance(subvalue, (int, float)) else str(subvalue)
            value_label = tk.Label(frame, text=formatted_subvalue, font=("Noto Sans Mono", 11), bg='black', fg='white')
            value_label.place(x=frame.frame_width - 20, y=y_offset, anchor='e')
            frame.widgets.append((key_label, value_label))
            y_offset += 30  # Move the next pair down by 30 px

    elif frame_id == "single":
        # Update regular frame
        formatted_value = f"{value:.1f}" if isinstance(value, (int, float)) else str(value)
        frame.value_label.config(text=formatted_value)

    elif frame_id == "percent":
        # Update percent frame
        if label == "RPM":
            percentage_width = (frame.frame_width - 20) * (value / 7000.0)  # Normalize RPM value to percentage
        else:
            percentage_width = (frame.frame_width - 20) * (value / 100.0)  # Normal percentage calculation

        frame.percent_box.config(width=percentage_width)

        formatted_value = f"{value:.1f}%" if label != "RPM" else f"{value:.0f} RPM"  # Show RPM value if label is RPM
        frame.value_label.config(text=formatted_value)


def collect_obd_data(update_queue):
    try:
        connection = obd.OBD()  # Auto-connects to USB or RF port
        if not connection.is_connected():
            raise Exception("Failed to connect to OBD-II device")

        # Map custom commands to obd.commands
        obd_commands = {cmd['Name']: getattr(obd.commands, cmd['Name'], None) for cmd in commands_list}

        with open('Tugrul_obd_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(['Timestamp', 'Command', 'Value', 'Mock Data'])

            while True:
                data_batch = {}
                for command in commands_list:
                    obd_cmd = obd_commands.get(command['Name'])
                    if obd_cmd is not None:
                        response = connection.query(obd_cmd)
                        if response.value is not None:
                            value = response.value
                            if hasattr(value, 'magnitude'):
                                value = float(value.magnitude)
                            data_batch[command['Name']] = value
                            writer.writerow([time.strftime("%m/%d/%y - %H:%M:%S"), command['Name'], str(value), "No"])
                        else:
                            data_batch[command['Name']] = "N/A"
                            writer.writerow([time.strftime("%m/%d/%y - %H:%M:%S"), command['Name'], "N/A", "No"])
                    else:
                        print(f"Command {command['Name']} not found in OBD library")

                data_batch["Mock Data"] = False
                processed_data = process_data(data_batch)
                update_queue.put(processed_data)
                time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        test_data(update_queue)


def distance_since_dtc_clear_generator():
    value = 500
    while True:
        yield value
        value += 0.025


def fuel_level_generator():
    value = 45
    while True:
        yield value
        value -= 0.01


distance_since_dtc_clear = distance_since_dtc_clear_generator()
fuel_level = fuel_level_generator()


def test_data(update_queue):
    keys = {
        "ENGINE_LOAD": lambda: random.uniform(0, 100),  # Example: Random value between 0 and 100
        "DISTANCE_SINCE_DTC_CLEAR": lambda: next(distance_since_dtc_clear),  # Starts from 500 and increments by 0.5
        "RPM": lambda: random.uniform(1000, 4000),  # Example: Random value between 1000 and 4000
        "SPEED": lambda: random.uniform(0, 120),  # Example: Random value between 0 and 120
        "FUEL_LEVEL": lambda: next(fuel_level),  # Starts from 45 and decrements by 0.1
        "AMBIANT_AIR_TEMP": lambda: random.uniform(-10, 30),  # Example: Random value between -10 and 30
        "THROTTLE_POS_B": lambda: random.uniform(0, 100),  # Example: Random value between 0 and 100
        "ACCELERATOR_POS_D": lambda: random.uniform(0, 100),  # Example: Random value between 0 and 100
        "ACCELERATOR_POS_E": lambda: random.uniform(0, 100),  # Example: Random value between 0 and 100
    }

    while True:
        data_batch = {key: generator() for key, generator in keys.items()}
        processed_data = process_data(data_batch)
        update_queue.put(processed_data)
        time.sleep(1)


def process_data(data_batch):
    global first_values  # Ensure we're modifying the global dictionary
    processed_data = {}

    for key, value in data_batch.items():
        if value == "N/A":
            continue  # Skip processing if data is not available

        if hasattr(value, 'magnitude'):
            value = float(value.magnitude)  # Convert Quantity to float

        # Apply conversions based on key
        if key == "SPEED":
            initial_distance = first_values.get("DISTANCE_SINCE_DTC_CLEAR")
            current_distance = data_batch.get("DISTANCE_SINCE_DTC_CLEAR")
            initial_time = first_values.get("time")
            current_time = time.strftime("%H:%M:%S")

            if initial_distance is not None and current_distance is not None and initial_time is not None:
                distance = current_distance - initial_distance

                # Calculate time difference in minutes
                initial_time_obj = datetime.strptime(initial_time, "%H:%M:%S")
                current_time_obj = datetime.strptime(current_time, "%H:%M:%S")
                time_diff = (current_time_obj - initial_time_obj).total_seconds() / 60.0
                time_diff = max(time_diff, 1)
                value = kmh_to_mph(value, time_diff, distance)
                frame_id = "dictionary"  # Regular frame
            else:
                value = rpm_to_rpm(value)
                frame_id = "single"  # Regular frame

        elif key == "AMBIANT_AIR_TEMP":
            value = celsius_to_fahrenheit(value)
            frame_id = "single"  # Regular frame

        elif key == "ENGINE_LOAD":
            value = rpm_to_rpm(value)
            frame_id = "percent"  # Dictionary frame

        elif key == "FUEL_LEVEL":
            initial_fuel_level = first_values.get("FUEL_LEVEL")
            initial_distance = first_values.get("DISTANCE_SINCE_DTC_CLEAR")
            current_distance = data_batch.get("DISTANCE_SINCE_DTC_CLEAR")

            if initial_fuel_level is not None and initial_distance is not None and current_distance is not None:
                distance = current_distance - initial_distance
                value = calculate_mpg(distance, initial_fuel_level, value)
                frame_id = "dictionary"
            else:
                value = rpm_to_rpm(value)
                frame_id = "single"  # Regular frame

        elif key == "DISTANCE_SINCE_DTC_CLEAR":
            value = calculate_distance(value)
            frame_id = "single"  # Dictionary frame

        elif key == "RPM":
            frame_id = "percent"  # Treat RPM as a percentage frame

        else:
            frame_id = "single"  # Default to regular frame

        if key not in first_values:
            first_values[key] = value  # Store the first read value

        # Add initial time to first_values if not already set
        if "time" not in first_values:
            first_values["time"] = time.strftime("%H:%M:%S")

        processed_data[key] = {'id': frame_id, 'data': value}

    return processed_data


if __name__ == "__main__":
    update_queue = queue.Queue()
    thread_data = threading.Thread(target=collect_obd_data, args=(update_queue,), daemon=True)
    thread_data.start()
    create_gui(update_queue)
