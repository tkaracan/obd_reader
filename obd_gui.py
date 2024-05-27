import tkinter as tk
import random

class InfoBox(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Info Box")
        self.geometry("300x200")

        self.info_labels = {}
        self.create_info_labels()
        self.update_info()

    def create_info_labels(self):
        # Create labels for each key-value pair
        keys = ["Value 1", "Value 2", "Value 3"]
        for i, key in enumerate(keys):
            label = tk.Label(self, text=f"{key}: ", anchor="w")
            label.pack(fill="x")
            self.info_labels[key] = label

    def update_info(self):
        # Update the values of the info labels with random numbers
        self.info_labels["Value 1"].config(text=f"Value 1: {random.randint(0, 100)}")
        self.info_labels["Value 2"].config(text=f"Value 2: {random.randint(0, 100)}")
        self.info_labels["Value 3"].config(text=f"Value 3: {random.randint(0, 100)}")

        # Schedule the next update after 1000 milliseconds (1 second)
        self.after(1000, self.update_info)

if __name__ == "__main__":
    info_box = InfoBox()
    info_box.mainloop()