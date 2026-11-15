import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


BASE_DIR = Path(__file__).resolve().parent

class MainWindow:
	
	def __init__(self):
		self.root = tk.Tk()
		self.root.title("Personal Expense Tracker")
		self.root.config(bg="#89f08c")

		# Creating a shortcut is optional and supported only on Windows.
		if sys.platform == "win32":
			menu_bar = tk.Menu(self.root)
			tools_menu = tk.Menu(menu_bar, tearoff=False)
			tools_menu.add_command(
				label="Create Desktop Shortcut",
				command=self.create_desktop_shortcut,
			)
			menu_bar.add_cascade(label="Tools", menu=tools_menu)
			self.root.config(menu=menu_bar)
		
		self.icon1 = tk.PhotoImage(file=str(BASE_DIR / "Dollar.png"))
		self.root.iconphoto(True, self.icon1)
		self.icon2 = tk.PhotoImage(file=str(BASE_DIR / "wallet.png")).subsample(7, 7)
		
		window_width = 800
		window_height = 600
		
		screen_width = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()
		
		self.root.wm_minsize(window_width, window_height)
		
		x = (screen_width - window_width) // 2
		y = (screen_height - window_height) // 2
		
		self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
		
		for col in range(10):
			self.root.grid_columnconfigure(col, weight=1)
		
		for row in range(15):
			self.root.grid_rowconfigure(row, weight=1)
		
		header_frame = tk.Frame(self.root, bg=self.root["background"])
		header_frame.grid(row=0, column=0, columnspan=6, sticky="ew")
		header_frame.grid_columnconfigure(0, weight=1)
		
		first_window_label = tk.Label(header_frame,
									  text="Be Mindful of Your Finances",
									  font=("Helvetica", 20, "bold"),
									  bg=self.root["background"],
									  padx=10,
									  pady=15,
									  image=self.icon2,
									  compound='right')
		
		first_window_label.grid(row=0, column=4, sticky='n')
		
		next_page_button = tk.Button(self.root, text='Generate Graph', font=('Helvetica', 15, "bold"), command=self.generate_graph)
		next_page_button.grid(row=15, column=10, padx=10, pady=10, sticky="n")
		
		apply_changes_button = tk.Button(self.root, text='Apply Changes', font=('Helvetica', 15, "bold"), command=self.apply_changes)
		apply_changes_button.grid(row=15, column=4, columnspan=3, padx=10, pady=10, sticky="new")
		
		import_button = tk.Button(self.root, text='Import File', font=('Helvetica', 13, "bold"), command=self.import_data)
		import_button.grid(row=14, column=4, padx=15, pady=5, sticky="nsew")
		
		save_button = tk.Button(self.root, text='Save File', font=('Helvetica', 13, "bold"), command=self.save_data)
		save_button.grid(row=14, column=5, padx=5, pady=5, sticky="nsew")
		
		days = [str(day) for day in range(1, 31)]
		selected_day = tk.StringVar()
		self.combobox = ttk.Combobox(self.root, textvariable=selected_day, values=days, state="readonly", font=('Helvetica', 13, "bold"))
		self.combobox.grid(row=1, column=4, columnspan=1, padx=10, pady=5)
		self.combobox.set("Choose Date")

		# Keep a visible reminder of the dates that have recorded entries.
		self.saved_days_hint = tk.StringVar(value="Recorded days: none")
		tk.Label(
			self.root,
			textvariable=self.saved_days_hint,
			wraplength=200,
			justify="center",
		).grid(row=2, column=4, padx=5, pady=5)

		self.combobox.bind("<<ComboboxSelected>>", self.update_entries) # "<<ComboboxSelected>>" is an event that triggers self.update_entries function
		
		self.entries = {
			"Food": tk.StringVar(),
			"Transport": tk.StringVar(),
			"Housing": tk.StringVar(),
			"Shopping": tk.StringVar(),
		}
		
		row = 1
		for category, var in self.entries.items():
			tk.Label(self.root, text=category, font=('Helvetica', 13, "bold")).grid(row=row, column=10, columnspan=2, padx=7, pady=7, sticky="nsew")
			tk.Entry(self.root, textvariable=var, font=('Helvetica', 14)).grid(row=row, column=5, columnspan=2, padx=7,pady=7, sticky="ns")
			row += 1
		
		self.collected_data = {}
		self.monthly_totals = {}
		
		self.root.mainloop()
  
	def create_desktop_shortcut(self):
		"""Create a Windows desktop shortcut to this copy of the app.

		The shortcut launches pythonw.exe from the same Python environment
		used to start the application, so no IDE or console is required.
		"""
		if sys.platform != "win32":
			messagebox.showinfo("Windows Only", "Desktop shortcuts are currently supported on Windows only.")
			return

		pythonw = Path(sys.executable).with_name("pythonw.exe")
		if not pythonw.is_file():
			messagebox.showerror(
				"Shortcut Not Created",
				"Could not find pythonw.exe in the active Python environment."
			)
			return

		# Use Windows' desktop folder rather than assuming ~/Desktop: it may
		# have been redirected to OneDrive or another location.
		ps_script = r"""$ErrorActionPreference = 'Stop'
$desktop = [Environment]::GetFolderPath('DesktopDirectory')
if (-not $desktop) { throw 'Could not locate the Desktop folder.' }
$shortcutPath = Join-Path $desktop 'Personal Expense Tracker.lnk'
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $env:EXPENSE_TRACKER_PYTHONW
$shortcut.Arguments = '"' + $env:EXPENSE_TRACKER_SCRIPT + '"'
$shortcut.WorkingDirectory = $env:EXPENSE_TRACKER_DIRECTORY
$shortcut.Description = 'Launch Personal Expense Tracker'
$shortcut.Save()"""

		env = os.environ.copy()
		env.update({
			"EXPENSE_TRACKER_PYTHONW": str(pythonw),
			"EXPENSE_TRACKER_SCRIPT": str(Path(__file__).resolve()),
			"EXPENSE_TRACKER_DIRECTORY": str(BASE_DIR),
		})
		try:
			result = subprocess.run(
				["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", ps_script],
				env=env,
				capture_output=True,
				text=True,
				errors="replace",
				creationflags=subprocess.CREATE_NO_WINDOW,
				timeout=20,
				check=True,
			)
		except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
			messagebox.showerror("Shortcut Not Created", f"Windows could not create the shortcut:\n{exc}")
			return
		messagebox.showinfo(
			"Shortcut Created",
			"A 'Personal Expense Tracker' shortcut was created on your desktop."
		)

	def get_data(self):
		category_data = {}
		current_date = self.combobox.get()
		
		for category, var in self.entries.items():
			value = var.get()
			if value == "":
				value = 0.0
			else:
				try:
					value = float(value)
				except ValueError:
					messagebox.showerror("Invalid Input", f"Please enter a number for {category}.")
					return None, None
				if not math.isfinite(value):
					messagebox.showerror("Invalid Input", f"Please enter a finite number for {category}.")
					return None, None
			category_data[category] = value
		return current_date, category_data
	
	def update_entries(self, event=None):
		
		current_date = self.combobox.get()
		
		if current_date in self.collected_data:
			data = self.collected_data[current_date]
			for cat, var in self.entries.items():
				var.set(data.get(cat, ""))
		else:
			for var in self.entries.values():
				var.set("")
			
	def apply_changes(self):
		
		date, data = self.get_data() # date = current_date; data = category_date
		if data is None:
			return
		
		if date == "Choose Date":
			messagebox.showinfo("Missing Date", "Please choose a date before applying changes.")
			return
		
		self.collected_data[date] = data
		self.monthly_totals = self.gather_all_data()
		self.update_saved_days_hint()

	def update_saved_days_hint(self):
		"""Display which dates have saved expense entries."""
		days = sorted(self.collected_data.keys(), key=int)
		if days:
			self.saved_days_hint.set("Recorded days: " + ", ".join(days))
		else:
			self.saved_days_hint.set("Recorded days: none")
		return days

	def gather_all_data(self):
		
		monthly_totals = {category: 0 for category in self.entries} # Dict comprehension (creating key-value pair where value is 0)
		for date_data in self.collected_data.values():
			for category, value in date_data.items():
				monthly_totals[category] += value
		return monthly_totals
		
	def generate_graph(self):
			categories = list(self.monthly_totals.keys())
			values = list(self.monthly_totals.values())
			
			filtered_categories = [cat for cat, val in zip(categories, values) if val > 0]
			filtered_values = [val for val in values if val > 0]
			
			if not filtered_values:
				messagebox.showinfo("No Data", "No data to display the graph!")
				return
			
			self.top = tk.Toplevel(self.root)
			self.top.title("Statistics")
			self.top.geometry("600x400")
			self.top.config(bg="#ede6d1")
			
			window_width = 600
			window_height = 400
			
			self.top.wm_minsize(window_width, window_height)
			self.top.grab_set()
		
			fig = Figure(figsize=(8, 6), dpi=120)
			fig.patch.set_facecolor('#ede6d1')
			ax = fig.add_subplot(111)
			ax.pie(filtered_values, labels=filtered_categories, autopct='%1.1f%%', startangle=90)
			ax.axis('equal')
			
			canvas = FigureCanvasTkAgg(fig, master=self.top)
			canvas.draw()
			canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
	
	def save_data(self):
		file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
		if not file_path:
			return
		try:
			with open(file_path, "w", encoding="utf-8") as f:
				json.dump(self.collected_data, f, indent=2)
		except OSError as exc:
			messagebox.showerror("Save Failed", f"Could not save the file:\n{exc}")
		else:
			messagebox.showinfo("Saved", f"Data saved to:\n{file_path}")
				
	def import_data(self):
		filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
		if not filename:
			return
		try:
			with open(filename, encoding="utf-8") as f:
				loaded_data = json.load(f)
			if not isinstance(loaded_data, dict):
				raise ValueError("Expected expense data to be a JSON object.")
			for day, categories in loaded_data.items():
				if day not in self.combobox["values"]:
					raise ValueError(f"Invalid day {day!r}. Choose a day from 1 to 30.")
				if not isinstance(categories, dict):
					raise ValueError(f"Invalid expense data for day {day}.")
				for category, value in categories.items():
					if category not in self.entries or type(value) not in (int, float) or not math.isfinite(value):
						raise ValueError(f"Invalid value for {category} on day {day}.")
		except (OSError, ValueError) as exc:
			messagebox.showerror("Import Failed", f"Could not import the file:\n{exc}")
			return
		self.collected_data = loaded_data
		self.monthly_totals = self.gather_all_data()
		days = self.update_saved_days_hint()
		if days:
			# Select an imported date so the user immediately sees the saved values.
			selected_day = days[0]
			self.combobox.set(selected_day)
			self.update_entries()
			messagebox.showinfo(
				"Import Successful",
				"Data imported successfully.\n\n"
				+ "Recorded days: " + ", ".join(days)
				+ f"\n\nDay {selected_day} has been selected automatically. "
				+ "To view other entries, choose another recorded day from the dropdown.",
			)
		else:
			self.combobox.set("Choose Date")
			self.update_entries()
			messagebox.showinfo("Import Complete", "The selected file contains no recorded days.")
	

if __name__ == '__main__':
	MainWindow()
