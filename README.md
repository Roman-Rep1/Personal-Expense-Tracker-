# Personal Expense Tracker

A lightweight **Python desktop application** for recording daily expenses, reviewing spending by category, and visualizing how money is spent. Built with **Python**, **Tkinter**, and **Matplotlib**.

## Features

- **Daily expense entry:** Record spending for a selected day (1–30).
- **Four expense categories:** Food, Transport, Housing, and Shopping.
- **Edit existing entries:** Select a previously used day to view and update its values.
- **Spending breakdown:** Generate a pie chart showing the proportion of expenses in each category.
- **JSON import/export:** Save expense data to a JSON file and load it again later. After import, the app lists the recorded days and automatically selects the first saved day.

## Tech stack

- **Python** — application logic and data processing
- **Tkinter / ttk** — desktop graphical user interface
- **Matplotlib** — pie-chart visualization
- **JSON** — file-based data storage

## Getting started

### Requirements

- Python 3.10 or newer, with Tkinter available
- A desktop environment (Windows, macOS, or Linux with Tk support)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Roman-Rep1/personal-expense-tracker.git
   cd personal-expense-tracker
   ```

2. (Optional) Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   On macOS/Linux, use `python3 -m venv .venv` and `source .venv/bin/activate` instead.

3. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Run the application from the project directory:

   ```powershell
   python Main.pyw
   ```

## Windows desktop shortcut (optional)

After installing the requirements and starting the application **from your Python virtual environment**, open **Tools → Create Desktop Shortcut** in the app. A **Personal Expense Tracker** shortcut will appear on your Windows desktop. You can use it to launch the app without opening VS Code, PyCharm, or a terminal.

The shortcut uses `pythonw.exe` from the Python environment that launched the app, and points to the local `Main.pyw` file. **Keep the project folder and its `.venv` in place**: moving or deleting either can break the shortcut. If you move the project, launch it from the new location and use **Tools → Create Desktop Shortcut** again. This shortcut option is Windows-only; it does not install Python or dependencies for other users.

The shortcut is **not created automatically** — you choose whether to create it. No additional Python package is required for this feature.

## How to use

1. Select a day from the dropdown menu.
2. Enter amounts in one or more expense categories.
3. Click **Apply Changes** to record the values.
4. Click **Generate Graph** to display a category breakdown.
5. Use **Save File** to export your data or **Import File** to load a previously saved JSON file. The app shows which days have recorded entries and selects the first saved day automatically. Use the date dropdown to view other recorded days.

**Note:** Click **Apply Changes** for each day before exporting. Only recorded entries are saved to the JSON file.

## Project structure

```text
personal-expense-tracker/
├── Main.pyw            # Desktop app and UI logic
├── Dollar.png          # Window icon
├── wallet.png          # Interface image
├── requirements.txt    # Third-party dependencies
├── .gitignore          # Files excluded from version control
├── screenshots/
│   ├── main-window.png  # Expense entry and recorded days
│   └── expense-chart.png # Spending breakdown pie chart
└── README.md
```

## Current limitations

- The date selector covers days **1–30** only; months and years are not tracked separately.
- Data is persisted only when explicitly exported to JSON.
- Desktop shortcuts can be created from within the app on Windows only; Python and dependencies must already be installed.

## Future improvements

Potential enhancements include a full calendar/date selector, configurable expense categories, automatic data persistence, input validation, and additional spending reports.
