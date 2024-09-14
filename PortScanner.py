import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext, filedialog
import socket
import csv

# Function to scan ports
def scan_ports(ip, start_port, end_port, output_text, progress_bar, results):
    total_ports = end_port - start_port + 1
    progress_bar['maximum'] = total_ports
    output_text.insert(tk.END, f"Scanning IP: {ip} from port {start_port} to {end_port}\n", 'light_green')

    for port in range(start_port, end_port + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            status = 'Open' if result == 0 else 'Closed'
            results.append([ip, port, status])
            # Use light_red tag for closed ports, light_green for open ports
            tag = 'light_green' if status == 'Open' else 'light_red'
            output_text.insert(tk.END, f"Port {port}: {status}\n", tag)
        except Exception as e:
            output_text.insert(tk.END, f"Error scanning port {port}: {e}\n", 'light_red')
        finally:
            try:
                sock.close()
            except Exception as e:
                output_text.insert(tk.END, f"Error closing socket for port {port}: {e}\n", 'light_red')
            progress_bar['value'] += 1
            root.update_idletasks()

    output_text.insert(tk.END, "Scan completed!\n", 'light_green')
    progress_bar['value'] = 0

# Function to start scanning
def start_scan(ip_entry, start_port_entry, end_port_entry, output_text, progress_bar):
    ip = ip_entry.get()
    try:
        start_port = int(start_port_entry.get())
        end_port = int(end_port_entry.get())
    except ValueError:
        output_text.insert(tk.END, "Invalid port number. Please enter valid integers.\n", 'light_red')
        return

    output_text.delete(1.0, tk.END)  # Clear previous output
    progress_bar['value'] = 0
    results = []

    # Start scanning in the main thread
    scan_ports(ip, start_port, end_port, output_text, progress_bar, results)

    # Save results to CSV file
    save_to_csv(results)

# Function to save results to CSV
def save_to_csv(results):
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['IP Address', 'Port', 'Status'])
                writer.writerows(results)
    except Exception as e:
        output_text.insert(tk.END, f"Error saving to CSV: {e}\n", 'light_red')

# Create the main window
root = tk.Tk()
root.title("Modern Port Scanner")
# Updated dimensions for a rectangular shape
root.geometry('800x600')  # Width x Height
root.configure(bg='#1e1e1e')  # Dark background for the window

# Use a modern sans-serif font
modern_font = ("Helvetica", 12)

# Add a frame for the inputs
input_frame = tk.Frame(root, bg='#2c2c2c', padx=10, pady=10, relief='ridge', borderwidth=2)
input_frame.pack(pady=20)

# Input Labels and Entries
tk.Label(input_frame, text="IP Address:", fg='white', bg='#2c2c2c', font=modern_font).grid(row=0, column=0, padx=5, pady=5, sticky="e")
ip_entry = tk.Entry(input_frame, font=modern_font, width=25, fg='white', bg='#3a3a3a', insertbackground='white')
ip_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Start Port:", fg='white', bg='#2c2c2c', font=modern_font).grid(row=1, column=0, padx=5, pady=5, sticky="e")
start_port_entry = tk.Entry(input_frame, font=modern_font, width=25, fg='white', bg='#3a3a3a', insertbackground='white')
start_port_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="End Port:", fg='white', bg='#2c2c2c', font=modern_font).grid(row=2, column=0, padx=5, pady=5, sticky="e")
end_port_entry = tk.Entry(input_frame, font=modern_font, width=25, fg='white', bg='#3a3a3a', insertbackground='white')
end_port_entry.grid(row=2, column=1, padx=5, pady=5)

# Scan Button
scan_button = tk.Button(root, text="Start Scan", font=modern_font, command=lambda: start_scan(ip_entry, start_port_entry, end_port_entry, output_text, progress_bar), bg='#4a4a4a', fg='white', relief='flat', padx=10, pady=5)
scan_button.pack(pady=10)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient='horizontal', length=760, mode='determinate')  # Adjust length to fit rectangular window
progress_bar.pack(pady=10)

# Output Box for Results
output_text = scrolledtext.ScrolledText(root, width=90, height=20, font=("Helvetica", 10), wrap=tk.WORD, bg='#2c2c2c', fg='white')  # Adjust width and height
output_text.pack(pady=10)

# Define custom colors for tags
output_text.tag_configure('light_green', foreground='#00ff00')  # For open ports
output_text.tag_configure('light_red', foreground='#ff0000')    # For closed ports

# Start the main loop
root.mainloop()
