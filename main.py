import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES

# Function to convert duration string to total seconds
def parse_duration(duration):
    hours = minutes = seconds = 0
    parts = duration.split()

    if len(parts) == 1:  # Handle single unit like "_s" or "__m"
        if 'h' in parts[0]:
            hours = int(parts[0][:-1])
        elif 'm' in parts[0]:
            minutes = int(parts[0][:-1])
        elif 's' in parts[0]:
            seconds = int(parts[0][:-1])

    elif len(parts) == 2:  # Two units like "18m 46s"
        minutes = int(parts[0][:-1])
        seconds = int(parts[1][:-1])

    elif len(parts) == 3:  # Three units like "1h 18m 46s"
        hours = int(parts[0][:-1])
        minutes = int(parts[1][:-1])
        seconds = int(parts[2][:-1])

    return hours * 3600 + minutes * 60 + seconds

# Function to process the uploaded file and update the result label
def process_file(file_path):
    try:
        df = pd.read_csv(file_path)
        df['duration_seconds'] = df['duration'].apply(parse_duration)
        total_seconds = df['duration_seconds'].sum()
        total_hours = total_seconds // 3600
        total_seconds %= 3600
        total_minutes = total_seconds // 60
        total_seconds %= 60

        result_text = f"Total Time Worked: {total_hours} hours, {total_minutes} minutes, and {total_seconds} seconds"
        result_label.config(text=result_text, state="normal")
        result_label.pack(pady=20, fill=tk.X)
        reset_button.pack(pady=10, fill=tk.X)
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}", state="normal")
        result_label.pack(pady=20, fill=tk.X)

# Function to open file dialog
def open_file_dialog():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv")],
        title="Select a CSV File"
    )
    if file_path:
        process_file(file_path)

# Function to handle dropped file
def on_drop(event):
    file_path = event.data.strip('{}')  # Clean up Windows file paths
    if file_path:
        process_file(file_path)

# Function to reset the result label and hide the reset button
def reset_result():
    result_label.pack_forget()  
    reset_button.pack_forget()

# Function to open the help window with custom colors
def open_help():
    help_window = tk.Toplevel(root)
    help_window.title("Help")
    help_window.geometry("400x250")
    
    help_text = tk.Text(help_window, wrap="word", padx=10, pady=10, font=("Helvetica", 12), bg="#2b2b2b", fg="white")
    help_text.insert(tk.END, (
        "Instructions:\n\n"
        "1. Go to the 'Earnings' page on the Outlier platform.\n"
        "2. Click on the earnings report that you want to know the hours for.\n"
        "3. Select 'Download CSV' at the top right of the earnings report.\n"
        "4. Upload the downloaded file using the 'Upload CSV' button to find out your total hours.\n"
    ))
    help_text.config(state="disabled")
    help_text.pack(pady=20, fill=tk.BOTH, expand=True)

# Function to open the credits window
def open_credits():
    credits_window = tk.Toplevel(root)
    credits_window.title("Credits")
    credits_window.geometry("300x150")
    
    credits_label = tk.Label(credits_window, text="Developed by Dathan\nVersion 1.0", padx=10, pady=10)
    credits_label.pack(pady=20)

# Set up the main window
root = TkinterDnD.Tk()
root.title("Outlier Hours Calculator - Made by Dathan")
root.geometry("600x400")
root.configure(bg="#2b2b2b")

# Use ttk theme for modern look
style = ttk.Style()
style.theme_use('clam')

# Title label
title_label = tk.Label(root, text="Outlier Hours Calculator", font=("Helvetica", 20, "bold"), bg="#2b2b2b", fg="white")
title_label.pack(pady=10, fill=tk.X)

# Frame for upload section
upload_frame = tk.Frame(root, bg="#2b2b2b")
upload_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Upload button
upload_button = ttk.Button(upload_frame, text="Upload CSV File", command=open_file_dialog)
upload_button.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

# Drag-and-drop label
drop_label = tk.Label(upload_frame, text="Drag and Drop a CSV File Here", padx=20, pady=20, bg="#505050", fg="white", relief="sunken")
drop_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Result label (hidden initially)
result_label = tk.Label(root, text="Total Time Worked: ", padx=20, pady=20, bg="#3b3b3b", fg="white", relief="groove")
result_label.pack_forget()

# Reset button (hidden initially)
reset_button = ttk.Button(root, text="Reset", command=reset_result)
reset_button.pack_forget()

# Register drop target
upload_frame.drop_target_register(DND_FILES)
upload_frame.dnd_bind('<<Drop>>', on_drop)

# Create a menu bar
menu_bar = tk.Menu(root)
menu_bar.add_command(label="Help", command=open_help)
menu_bar.add_command(label="Credits", command=open_credits)
root.config(menu=menu_bar)

# Run the application
root.mainloop()
