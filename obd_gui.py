import tkinter as tk
import random


class InfoBox(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Info Box")
        self.geometry("500x500")

        self.info_frames = {}
        self.create_info_frames()
        self.update_info()

    def create_info_frames(self):
        # Create frames for each key in a 2x2 grid
        keys = ["Value 1", "Value 2", "Value 3", "Value 4"]
        for i, key in enumerate(keys):
            frame = tk.Frame(self, borderwidth=2, relief="groove")
            frame.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="nsew")

            label = tk.Label(frame, text=f"{key}: ", anchor="w")
            label.pack(fill="x")

            self.info_frames[key] = frame

        # Configure grid weights for equal distribution
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def generate_random_data(self, key):
        # Generate random data based on the key
        if key == "Value 1":
            return random.randint(0, 100)
        elif key == "Value 2":
            return random.uniform(0, 10)
        elif key == "Value 3":
            return random.choice(["Option A", "Option B", "Option C"])
        elif key == "Value 4":
            return random.randint(1000, 9999)
        else:
            return "Unknown"

    def update_info(self):
        # Update the values of the info labels in each frame with random data
        for key, frame in self.info_frames.items():
            random_data = self.generate_random_data(key)
            label = frame.winfo_children()[0]  # Assuming the label is the first child of the frame
            label.config(text=f"{key}: {random_data}")

        # Schedule the next update after 1000 milliseconds (1 second)
        self.after(1000, self.update_info)


if __name__ == "__main__":
    info_box = InfoBox()
    info_box.mainloop()