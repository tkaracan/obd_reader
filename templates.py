import tkinter as tk

def frame_single(root, frame_width, frame_height, label, row, col):
    frame = tk.Frame(root, width=frame_width, height=frame_height, bg='black')
    frame.place(x=(col + 1) * 10 + col * frame_width, y=(row + 1) * 10 + row * frame_height)
    frame.initialized = True
    frame.key_label = tk.Label(frame, text=label, font=("Noto Sans Mono", 10), bg='black', fg='white', anchor='nw')
    frame.key_label.place(x=10, y=10)
    frame.value_label = tk.Label(frame, text="", font=("Noto Sans Mono", 20), bg='black', fg='white')
    frame.value_label.place(relx=0.5, rely=0.5, anchor='center')
    return frame