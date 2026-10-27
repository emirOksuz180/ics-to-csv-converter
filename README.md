# Google Calendar ICS to CSV Converter

A lightweight, zero-dependency, user-friendly Python desktop tool designed to convert Google Calendar `.ics` export files into clean, Excel-compatible `.csv` format locally.

---

## Features

- **100% Local & Privacy-Friendly:** Runs entirely on your machine. No external APIs, no internet connection required, and zero data privacy risks.
- **Interactive File Explorer:** No need to deal with complex console path typing; standard Windows File Explorer dialogs let you pick your files effortlessly.
- **2-Step Safe Process:** Analyzes your calendar file first, shows you the total event count, and asks for your confirmation (`y/N`) before exporting.
- **Smart Focus Management:** Automatically brings the console back to focus after graphical windows close, allowing seamless keyboard interaction.
- **Zero Dependencies for End-Users:** Built using Python's built-in standard libraries (`csv`, `datetime`, `os`, `tkinter`).

---

## How to Use (For Users)

1. Go to **Google Calendar Settings** and export your calendar to get the `.ics` file.
2. Run the application (`.exe` or script).
3. Press **Enter** to open the File Explorer and select your `.ics` file.
4. Review the analyzed event count and type `y` to proceed.
5. Choose where to save your clean `.csv` file using the Save As dialog.
6. Press **Enter** to exit when finished!

---

## How to Run from Source (For Developers)

If you want to run or modify the Python script directly:

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/ics-to-csv-converter.git](https://github.com/YOUR_USERNAME/ics-to-csv-converter.git)
   cd ics-to-csv-converter