import pytz
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox


def convert_timezone(dt, from_tz, to_tz):
    from_zone = pytz.timezone(from_tz)
    to_zone = pytz.timezone(to_tz)

    dt = from_zone.localize(dt)
    utc_dt = dt.astimezone(pytz.utc)
    target_dt = utc_dt.astimezone(to_zone)
    return target_dt


def adjust_date(offset):
    current_date = datetime.now()
    new_date = current_date + timedelta(days=offset)
    time_entry.delete(0, tk.END)
    time_entry.insert(0, new_date.strftime('%H:%M:%S'))


def convert_time():
    from_tz = from_timezone_combobox.get()
    to_tz = to_timezone_combobox.get()

    try:
        time_str = time_entry.get()
        dt = datetime.strptime(time_str, '%H:%M:%S')
        dt = dt.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)

        converted_dt = convert_timezone(dt, from_tz, to_tz)

        # Check if the converted time is on the next day (+1) or the previous day (-1)
        date_difference = converted_dt.date() - datetime.now().date()

        if date_difference.days > 0:
            date_label.config(text="+1")
        elif date_difference.days < 0:
            date_label.config(text="-1")
        else:
            date_label.config(text="Same Day")

        result_label.config(text=f"Converted time: {converted_dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
    except ValueError:
        messagebox.showerror("Error", "Invalid time format!")


# Create main window
root = tk.Tk()
root.title("Time Zone Converter")

# Create widgets
from_timezone_label = ttk.Label(root, text="From Time Zone:")
from_timezone_label.grid(row=0, column=0, padx=10, pady=10)

from_timezone_combobox = ttk.Combobox(root, values=pytz.all_timezones, width=50)
from_timezone_combobox.grid(row=0, column=1, padx=10, pady=10)
from_timezone_combobox.set('UTC')  # Default value

to_timezone_label = ttk.Label(root, text="To Time Zone:")
to_timezone_label.grid(row=1, column=0, padx=10, pady=10)

to_timezone_combobox = ttk.Combobox(root, values=pytz.all_timezones, width=50)
to_timezone_combobox.grid(row=1, column=1, padx=10, pady=10)
to_timezone_combobox.set('Asia/Kolkata')  # Default value

time_label = ttk.Label(root, text="Enter Time (HH:MM:SS):")
time_label.grid(row=2, column=0, padx=10, pady=10)

time_entry = ttk.Entry(root, width=40)
time_entry.grid(row=2, column=1, padx=10, pady=10)

convert_button = ttk.Button(root, text="Convert", command=convert_time)
convert_button.grid(row=4, column=0, columnspan=2, pady=20)

result_label = ttk.Label(root, text="")
result_label.grid(row=5, column=0, columnspan=2)

date_label = ttk.Label(root, text="")
date_label.grid(row=6, column=0, columnspan=2)

root.mainloop()
