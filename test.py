import tkinter as tk

def create_grid(window):
    for row in range(3):
        for column in range(3):
            label = tk.Label(window, text="Hi", font=('Arial', 20), bg='sky blue')
            label.grid(row=row, column=column, sticky="nsew", padx=2, pady=2)

def main():
    root = tk.Tk()
    root.title("Tkinter Grid Test")
    root.geometry("900x600")

    # Make the grid cells expand to fill the window
    for i in range(3):
        root.grid_rowconfigure(i, weight=1)
        root.grid_columnconfigure(i, weight=1)

    create_grid(root)
    root.mainloop()

if __name__ == "__main__":
    main()



def process_data(data_batch):
    global first_values  # Ensure we're modifying the global dictionary
    is_mock_data = data_batch.pop("Mock Data", False)
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