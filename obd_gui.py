import tkinter as tk
import random


class InfoBox(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Info Box")
        self.height = 500
        self.width = 800
        self.columns = 2
        self.padding = 5
        self.geometry(f"{self.width}x{self.height}")

        self.info_frames = {}
        self.create_info_frames()
        self.update_info()

    def create_info_frames(self):
        # Create frames for each key in a 2x2 grid
        keys = ["Value 1", "Value 2", "Value 3", "Value 4"]
        designs = [1, 2, 2, 1]  # Specify the design for each key
        frame_width = (self.width - (self.columns + 1) * self.padding) / self.columns
        frame_height = (self.height - (len(keys) // self.columns + 1) * self.padding) / (len(keys) // self.columns)


        for i, (key, design) in enumerate(zip(keys, designs)):
            frame = tk.Frame(self, width=frame_width, height=frame_height, borderwidth=1, relief="groove")
            frame.grid(row=i // 2, column=i % 2, padx=self.padding, pady=self.padding)
            frame.grid_propagate(False)  # Disable grid propagation to maintain fixed size

            if design == 1:
                frame.initialized = True
                frame.key_label = tk.Label(frame, text=key, font=("Noto Sans Mono", 10), bg='black', fg='white',
                                           anchor='nw')
                frame.key_label.place(x=10, y=10)
                frame.value_label = tk.Label(frame, text="", font=("Noto Sans Mono", 20), bg='black', fg='white')
                frame.value_label.place(relx=0.5, rely=0.5, anchor='center')
            elif design == 2:
                label = tk.Label(frame, text=f"{key}: ", font=("Arial", 16))
                label.place(relx=0.5, rely=0.5, anchor="center")

            self.info_frames[key] = frame

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
        # Update the values in each frame with random data based on the design
        for key, frame in self.info_frames.items():
            random_data = self.generate_random_data(key)

            if key in ["Value 1", "Value 4"]:  # Design 1
                value_label = frame.winfo_children()[0]
                value_label.config(text=str(random_data))
            else:  # Design 2
                label = frame.winfo_children()[0]
                label.config(text=f"{key}: {random_data}")

        # Schedule the next update after 1000 milliseconds (1 second)
        self.after(1000, self.update_info)


if __name__ == "__main__":
    info_box = InfoBox()
    info_box.mainloop()