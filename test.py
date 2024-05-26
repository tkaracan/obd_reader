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