import tkinter as tk

def update_frame(frame, label, frame_id, value):
    # Decide which function to use based on frame_id
    if frame_id == "dictionary":
        update_dictionary_frame(frame, value)
    elif frame_id == "single":
        update_single_frame(frame, label, value)
    elif frame_id == "percent":
        update_percent_frame(frame, label, value)

def update_dictionary_frame(frame, value):
    if not hasattr(frame, 'initialized') or not frame.initialized:
        clear_frame_widgets(frame)
        frame.initialized = True
        frame.widgets = []
    y_offset = 25
    for subkey, subvalue in value.items():
        create_label_pair(frame, subkey, subvalue, y_offset)
        y_offset += 30

def update_single_frame(frame, label, value):
    if not hasattr(frame, 'initialized') or not frame.initialized:
        clear_frame_widgets(frame)
        frame.key_label = tk.Label(frame, text=label, font=("Noto Sans Mono", 10), bg='black', fg='white', anchor='nw')
        frame.key_label.place(x=10, y=10)
        frame.value_label = tk.Label(frame, text="", font=("Noto Sans Mono", 20), bg='black', fg='white')
        frame.value_label.place(relx=0.5, rely=0.5, anchor='center')
        frame.initialized = True
    frame.value_label.config(text=f"{value:.1f}" if isinstance(value, (int, float)) else str(value))

def update_percent_frame(frame, label, value):
    if not hasattr(frame, 'initialized') or not frame.initialized:
        clear_frame_widgets(frame)
        frame.key_label = tk.Label(frame, text=label, font=("Noto Sans Mono", 10), bg='black', fg='white', anchor='nw')
        frame.key_label.place(x=10, y=10)
        frame.percent_box = tk.Frame(frame, bg='white', height=frame.winfo_height() - 90, width=0)
        frame.percent_box.place(relx=0, rely=0.5, anchor='w')
        frame.value_label = tk.Label(frame, text="", font=("Noto Sans Mono", 20), bg='black', fg='white')
        frame.value_label.place(relx=0.5, rely=0.5, anchor='center')
        frame.initialized = True
    percentage_width = (frame.winfo_width() - 20) * (value / (7000.0 if label == "RPM" else 100.0))
    frame.percent_box.config(width=percentage_width)
    formatted_value = f"{value:.0f} RPM" if label == "RPM" else f"{value:.1f}%"
    frame.value_label.config(text=formatted_value)

def clear_frame_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_label_pair(frame, key, value, y_offset):
    key_label = tk.Label(frame, text=f"{key}", font=("Noto Sans Mono", 10), bg='black', fg='white')
    key_label.place(x=20, y=y_offset, anchor='w')
    value_label = tk.Label(frame, text=f"{value:.1f}" if isinstance(value, (int, float)) else str(value),
                           font=("Noto Sans Mono", 11), bg='black', fg='white')
    value_label.place(x=frame.winfo_width() - 20, y=y_offset, anchor='e')
    frame.widgets.append((key_label, value_label))
