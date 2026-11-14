import tkinter as tk

window = tk.Tk()

window_width = 800
window_height = 600

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.title("Financial Tracker")

window.mainloop()


