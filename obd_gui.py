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
        self.info_frames = {}
        self.create_info_frames()
        self.update_info()

    def create_info_frames(self):
        subkeys = ["Subkey 1", "Subkey 2", "Subkey 3"]
        values = {"bottom": 0, "top": 100}

        keys = ["Value 1", "Value 2", "Value 3", "Value 4"]
        designs = ["single", "multiple", "multiple", "percent"]
        frame_subkeys = [None, subkeys, subkeys, values]

        frame_width = (self.width - (self.columns + 1) * self.padding) / self.columns
        frame_height = (self.height - (len(keys) // self.columns + 1) * self.padding) / (len(keys) // self.columns)

        for i, (key, design, subkeys) in enumerate(zip(keys, designs, frame_subkeys)):
            frame = tk.Frame(self, width=frame_width, height=frame_height, bg='black', relief="groove",
                             highlightbackground="white",
                             highlightthickness=1)  # Set frame background to black and border to white
            frame.grid(row=i // 2, column=i % 2, padx=self.padding, pady=self.padding)
            frame.grid_propagate(False)

            if design == "single":
                frame.initialized = True
                frame.value_label = tk.Label(frame, text=key, font=("Noto Sans Mono", 20), bg='black', fg='white',
                                             anchor='nw')
                frame.value_label.place(relx=0.5, rely=0.5, anchor='center')
                frame.key_label = tk.Label(frame, text=f"{key}: ", font=("Noto Sans Mono", 10), bg='black', fg='white')
                frame.key_label.place(x=10, y=10)
            elif design == "multiple":
                frame.initialized = True
                frame.key_labels = {}
                frame.value_labels = {}
                frame.data = {}

                frame.key_label = tk.Label(frame, text=f"{key}: ", font=("Noto Sans Mono", 10), bg='black', fg='white')
                frame.key_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="w")

                for j, sub_key in enumerate(subkeys):
                    key_label = tk.Label(frame, text=sub_key, font=("Noto Sans Mono", 12), anchor="e", bg='black',
                                         fg='white')
                    key_label.grid(row=j + 1, column=0, padx=(10, 5), pady=(10 if j == 0 else 5, 5), sticky="e")
                    frame.key_labels[sub_key] = key_label

                    value_label = tk.Label(frame, text="", font=("Noto Sans Mono", 12), anchor="w", bg='black',
                                           fg='white')
                    value_label.grid(row=j + 1, column=1, padx=(5, 10), pady=(10 if j == 0 else 5, 5), sticky="w")
                    frame.value_labels[sub_key] = value_label

            elif design == "percent":
                frame.initialized = True
                frame.key_label = tk.Label(frame, text=f"{key}: ", font=("Noto Sans Mono", 10), bg='black', fg='white')
                frame.key_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="w")

                frame.value_label = tk.Label(frame, text=key, font=("Noto Sans Mono", 20), bg='white', fg='black',
                                             anchor='nw')
                frame.value_label.place(relx=0.5, rely=0.5, anchor='center')

                frame.percent_box = tk.Frame(frame, width=frame_width, height=frame_height / 3, bg='white')
                frame.percent_box.place(relx=0, rely=0.5, anchor='w')

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