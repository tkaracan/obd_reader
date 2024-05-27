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
        keys = ["Value 1", "Value 2", "Value 3", "Value 4"]
        designs = [1, 2, 2, 1]

        frame_width = (self.width - (self.columns + 1) * self.padding) / self.columns
        frame_height = (self.height - (len(keys) // self.columns + 1) * self.padding) / (len(keys) // self.columns)

        for i, (key, design) in enumerate(zip(keys, designs)):
            frame = tk.Frame(self, width=frame_width, height=frame_height, borderwidth=1, relief="groove")
            frame.grid(row=i // 2, column=i % 2, padx=self.padding, pady=self.padding)
            frame.grid_propagate(False)

            if design == 1:
                frame.initialized = True
                frame.key_label = tk.Label(frame, text=key, font=("Noto Sans Mono", 20), bg='black', fg='white', anchor='nw')
                frame.key_label.place(relx=0.5, rely=0.5, anchor='center')
                frame.value_label = tk.Label(frame, text=f"{key}: ", font=("Noto Sans Mono", 10), bg='black', fg='white')
                frame.value_label.place(x=10, y=10)
            elif design == 2:
                frame.key_labels = {}
                frame.value_labels = {}
                frame.data = {}

                for j, sub_key in enumerate(["Subkey 1", "Subkey 2", "Subkey 3"]):
                    key_label = tk.Label(frame, text=sub_key, font=("Arial", 12, "bold"), anchor="e")
                    key_label.grid(row=j, column=0, padx=(10, 5), pady=5, sticky="e")
                    frame.key_labels[sub_key] = key_label

                    value_label = tk.Label(frame, text="", font=("Arial", 12), anchor="w")
                    value_label.grid(row=j, column=1, padx=(5, 10), pady=5, sticky="w")
                    frame.value_labels[sub_key] = value_label

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
            return random.randint(1000, 9999)
        else:
            return "Unknown"

    def update_info(self):
        for key, frame in self.info_frames.items():
            random_data = self.generate_random_data(key)

            if key in ["Value 1", "Value 4"]:
                value_label = frame.winfo_children()[0]
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