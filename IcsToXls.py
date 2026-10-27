import ctypes
import csv
from datetime import datetime
import os
import platform
import tkinter as tk
from tkinter import filedialog


def bring_console_to_front():
  """Forces the console window to regain focus on Windows after a GUI dialog closes."""
  if platform.system() == "Windows":
    try:
      kernel32 = ctypes.windll.kernel32
      user32 = ctypes.windll.user32
      hwnd = kernel32.GetConsoleWindow()
      if hwnd:
        user32.SetForegroundWindow(hwnd)
    except Exception:
      pass


def parse_ics_date(date_str):
  if not date_str:
    return ""
  date_str = str(date_str).strip()
  try:
    if "T" in date_str:
      dt = datetime.strptime(date_str.split(".")[0], "%Y%m%dT%H%M%S")
      return dt.strftime("%Y-%m-%d %H:%M")
    else:
      dt = datetime.strptime(date_str, "%Y%m%d")
      return dt.strftime("%Y-%m-%d")
  except Exception:
    return date_str


def main():
  print("==================================================")
  print("      Google Calendar ICS to CSV Converter        ")
  print("==================================================\n")
  print("This tool converts your Google Calendar .ics export file")
  print("into a clean, Excel-compatible .csv file locally.\n")

  # Wait for user confirmation before popping up graphical windows
  input("Press [Enter] to select your Google Calendar .ics file...")

  # --- STEP 1: Select and Read ICS File ---
  print("\n[Step 1/2] Opening File Explorer to select .ics file...")

  root = tk.Tk()
  root.withdraw()
  ics_file_path = filedialog.askopenfilename(
      title="Step 1: Select Google Calendar .ics File",
      filetypes=[("iCalendar Files", "*.ics"), ("All Files", "*.*")],
  )
  root.destroy()  # Completely destroy the root window to release focus
  bring_console_to_front()  # Force focus back to the console

  if not ics_file_path or not os.path.exists(ics_file_path):
    print("\n[Error] No valid .ics file selected or file not found.")
    input("\nPress [Enter] to exit...")
    return

  print(f"-> Selected File: {ics_file_path}")

  # Parse the ICS file to preview events
  events = []
  current_event = {}
  in_event = False

  try:
    print("-> Analyzing calendar file, please wait...")
    with open(ics_file_path, "r", encoding="utf-8", errors="ignore") as f:
      for line in f:
        line = line.strip()
        if line == "BEGIN:VEVENT":
          in_event = True
          current_event = {}
        elif line == "END:VEVENT":
          in_event = False
          events.append(current_event)
        elif in_event:
          if line.startswith("SUMMARY:"):
            current_event["Summary"] = line[8:]
          elif line.startswith("DTSTART"):
            current_event["Start"] = parse_ics_date(line.split(":")[-1])
          elif line.startswith("DTEND"):
            current_event["End"] = parse_ics_date(line.split(":")[-1])
          elif line.startswith("LOCATION:"):
            current_event["Location"] = line[9:]
          elif line.startswith("DESCRIPTION:"):
            current_event["Description"] = line[12:].replace("\\n", " ")
  except Exception as e:
    print(f"\n[Error] Failed to read the .ics file: {e}")
    input("\nPress [Enter] to exit...")
    return

  print(
      f"-> Successfully analyzed! Found {len(events)} events in the calendar."
  )

  # Ask user with y/N if they want to proceed (Focus is now guaranteed to be here)
  confirm = (
      input(
          "\nDo you want to proceed with exporting these events to CSV? (y/N): "
      )
      .strip()
      .lower()
  )
  if confirm != "y":
    print("\n[Cancelled] Operation aborted by the user.")
    input("\nPress [Enter] to exit...")
    return

  # --- STEP 2: Choose Output and Save ---
  print(
      "\n[Step 2/2] Opening File Explorer to choose where to save the .csv"
      " file..."
  )
  default_dir = os.path.dirname(ics_file_path)

  root = tk.Tk()
  root.withdraw()
  csv_file_path = filedialog.asksaveasfilename(
      title="Step 2: Save Converted CSV File As",
      initialdir=default_dir,
      defaultextension=".csv",
      filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
      initialfile="calendar_events.csv",
  )
  root.destroy()  # Destroy root window here too
  bring_console_to_front()  # Force focus back to the console

  if not csv_file_path:
    print("\n[Cancelled] No output location selected. Operation aborted.")
    input("\nPress [Enter] to exit...")
    return

  # Write to CSV file
  try:
    with open(
        csv_file_path, mode="w", newline="", encoding="utf-8-sig"
    ) as csv_file:
      writer = csv.writer(csv_file, delimiter=";")
      writer.writerow(["Event Name", "Start", "End", "Location", "Description"])

      for ev in events:
        writer.writerow([
            ev.get("Summary", ""),
            ev.get("Start", ""),
            ev.get("End", ""),
            ev.get("Location", ""),
            ev.get("Description", ""),
        ])

    print(
        f"\n[Success] {len(events)} events successfully exported to:"
        f" '{csv_file_path}'."
    )
  except Exception as e:
    print(f"\n[Error] Failed to write the CSV file: {e}")

  # Exit prompt
  input("\nPress [Enter] to exit...")


if __name__ == "__main__":
  main()