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
        self.configure(bg='black')  # Set the background color of the whole screen to black

        # Initialize design variables before creating frames
        self.key_font_size = 20
        self.bg_color = 'white'
        self.fg_color = 'black'

        self.info_frames = {}
        self.create_info_frames()  # Now safe to call after setting attributes
        self.update_info()


    def create_info_frames(self):
        subkeys = ["Subkey 1", "Subkey 2", "Subkey 3"]
        values = {"bottom": 0, "top": 100}

        keys = ["Value 1", "Value 2", "Value 3", "Value 4"]
        designs = ["single", "multiple", "multiple", "percent"]
        frame_subkeys = [None, subkeys, subkeys, values]

        frame_width = (self.width - (self.columns + 2) * self.padding) / self.columns
        frame_height = (self.height - (len(keys) // self.columns + 2) * self.padding) / (len(keys) // self.columns)

        for i, (key, design, subkeys) in enumerate(zip(keys, designs, frame_subkeys)):
            frame = tk.Frame(self, width=frame_width, height=frame_height, bg='black', relief="groove",
                             highlightbackground="white",
                             highlightthickness=1)
            frame.grid(row=i // 2, column=i % 2, padx=self.padding, pady=self.padding)
            frame.grid_propagate(False)

            # Use variables for key label design
            frame.key_label = tk.Label(frame, text=f"{key}: ", font=("Noto Sans Mono", self.key_font_size), bg=self.bg_color, fg=self.fg_color)
            frame.key_label.place(x=10, y=10)

            if design == "single":
                frame.initialized = True
                frame.value_label = tk.Label(frame, text=key, font=("Noto Sans Mono", 40), bg=self.bg_color, fg=self.fg_color,
                                             anchor='nw')
                frame.value_label.place(relx=0.5, rely=0.5, anchor='center')

            elif design == "multiple":
                frame.initialized = True
                frame.key_labels = {}
                frame.value_labels = {}
                frame.data = {}

                # Title label for the key
                frame.key_label = tk.Label(frame, text=f"{key}: ", font=("Noto Sans Mono", self.key_font_size),
                                           bg=self.bg_color, fg=self.fg_color)
                frame.key_label.place(x=10, y=10)

                y_offset = 50  # Start placing at 50 px vertically

                for sub_key in subkeys:
                    # Subkey labels
                    key_label = tk.Label(frame, text=sub_key + ":", font=("Noto Sans Mono", 12), anchor="w",
                                         bg=self.bg_color, fg=self.fg_color)
                    key_label.place(x=20, y=y_offset, anchor="w")
                    frame.key_labels[sub_key] = key_label

                    # Value labels
                    value_label = tk.Label(frame, text="", font=("Noto Sans Mono", 12), anchor="e", bg=self.bg_color,
                                           fg=self.fg_color)
                    value_label.place(x=frame.winfo_width() - 20, y=y_offset, anchor="e")
                    frame.value_labels[sub_key] = value_label

                    y_offset += 30  # Increment the vertical offset for the next subkey-value pair



            elif design == "percent":
                frame.initialized = True
                frame.percent_box = tk.Frame(frame, width=frame_width, height=frame_height / 3, bg=self.bg_color)
                frame.percent_box.place(relx=0, rely=0.5, anchor='w')
                frame.value_label = tk.Label(frame, text=key, font=("Noto Sans Mono", 20), bg=self.bg_color, fg=self.fg_color,
                                             anchor='nw')
                frame.value_label.place(relx=0.5, rely=0.5, anchor='center')

            self.info_frames[key] = frame

    def generate_random_data(self, key):
        if key == "Value 1":
            return random.randint(0, 100)
        elif key == "Value 2":
            return {
                "Subkey 1": random.randint(0, 100),
                "Subkey 2": random.uniform(0, 10),
                "Subkey 3": random.choice(["Option X", "Option Y", "Option Z"])
            }
        elif key == "Value 3":
            return {
                "Subkey 1": random.randint(1000, 9999),
                "Subkey 2": random.uniform(100, 1000),
                "Subkey 3": random.choice(["Option A", "Option B", "Option C"])
            }
        elif key == "Value 4":
            return {"value": random.randint(0, 100), "top": 100, "bottom": 0}
        else:
            return "Unknown"

    def update_info(self):
        for key, frame in self.info_frames.items():
            random_data = self.generate_random_data(key)

            if key in ["Value 1", "Value 4"]:
                if key == "Value 4":
                    top_value = random_data["top"]
                    bottom_value = random_data["bottom"]
                    value = random_data["value"]
                    percentage = (value - bottom_value) / (top_value - bottom_value)
                    new_width = max(1, int(frame.winfo_width() * percentage))
                    frame.percent_box.configure(width=new_width)

                    # Update the value label with the percentage
                    frame.value_label.config(text=f"{percentage:.0%}")
                else:
                    value_label = frame.value_label
                    value_label.config(text=str(random_data))
            else:
                frame.data.update(random_data)
                for sub_key, value in frame.data.items():
                    value_label = frame.value_labels[sub_key]
                    value_label.config(text=str(value))

        self.after(1000, self.update_info)


if __name__ == "__main__":
    info_box = InfoBox()
    info_box.mainloop()