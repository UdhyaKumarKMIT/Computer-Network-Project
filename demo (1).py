import tkinter as tk
from tkinter import messagebox
import os

# Path to the hosts file (Windows and Linux/Mac compatible)
hosts_path = r"C:\Windows\System32\drivers\etc\hosts" if os.name == 'nt' else '/etc/hosts'

# IP address to redirect blocked domains to (localhost)
redirect_ip = "127.0.0.1"

# Initialize theme as light mode
current_theme = "light"

# Colors for light and dark mode
light_theme_colors = {
    "bg": "#f5f5f5",
    "fg": "#333333",
    "button_bg": "#3498db",
    "button_fg": "white",
    "entry_bg": "#ffffff",
    "entry_fg": "#333333",
    "header_bg": "#2980b9",
    "header_fg": "white"
}

dark_theme_colors = {
    "bg": "#2c3e50",
    "fg": "#ecf0f1",
    "button_bg": "#34495e",
    "button_fg": "white",
    "entry_bg": "#34495e",
    "entry_fg": "#ecf0f1",
    "header_bg": "#2c3e50",
    "header_fg": "#ecf0f1"
}

# Function to block a domain
def block_domain():
    domain = domain_field.get().strip()  # Get the input domain name

    if not domain:
        messagebox.showerror("Error", "Please enter a domain name!")
        return

    try:
        # Check if domain is already blocked
        with open(hosts_path, 'r') as file:
            if domain in file.read():
                messagebox.showinfo("Info", f"{domain} is already blocked!")
                return

        # Add the domain to the hosts file
        with open(hosts_path, 'a') as file:
            file.write(f"{redirect_ip} {domain}\n")
        
        messagebox.showinfo("Success", f"{domain} has been blocked!")
    except PermissionError:
        messagebox.showerror("Error", "Permission denied! Please run the script as administrator.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to unblock a domain
def unblock_domain():
    domain = domain_field.get().strip()  # Get the input domain name

    if not domain:
        messagebox.showerror("Error", "Please enter a domain name!")
        return

    try:
        with open(hosts_path, 'r') as file:
            lines = file.readlines()

        # Filter out the blocked domain
        with open(hosts_path, 'w') as file:
            for line in lines:
                if domain not in line:  # Write all lines except the one containing the domain
                    file.write(line)

        messagebox.showinfo("Success", f"{domain} has been unblocked!")
    except PermissionError:
        messagebox.showerror("Error", "Permission denied! Please run the script as administrator.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to toggle between light and dark mode
def toggle_theme():
    global current_theme

    if current_theme == "light":
        current_theme = "dark"
        set_theme(dark_theme_colors)
    else:
        current_theme = "light"
        set_theme(light_theme_colors)

# Function to apply the theme colors
def set_theme(theme_colors):
    root.config(bg=theme_colors["bg"])
    header.config(bg=theme_colors["header_bg"], fg=theme_colors["header_fg"])
    label.config(bg=theme_colors["bg"], fg=theme_colors["fg"])
    domain_field.config(bg=theme_colors["entry_bg"], fg=theme_colors["entry_fg"])
    block_button.config(bg=theme_colors["button_bg"], fg=theme_colors["button_fg"])
    unblock_button.config(bg=theme_colors["button_bg"], fg=theme_colors["button_fg"])
    toggle_button.config(bg=theme_colors["button_bg"], fg=theme_colors["button_fg"])

# Create the tkinter window
root = tk.Tk()
root.title("Block/Unblock Domain")

# Set window size and center it
window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height/2 - window_height/2)
position_right = int(screen_width/2 - window_width/2)
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# Header label
header = tk.Label(root, text="Domain Blocker", font=("Helvetica", 16, "bold"), pady=10)
header.pack(fill="x")

# Domain input label and field
label = tk.Label(root, text="Enter domain to block/unblock:", font=("Helvetica", 12))
label.pack(pady=10)
domain_field = tk.Entry(root, width=35, font=("Helvetica", 12), bd=2, relief="groove")
domain_field.pack(pady=5)

# Style for the buttons
button_style = {"font": ("Helvetica", 12), "bd": 0, "width": 20, "pady": 5}

# Block and Unblock buttons with rounded corners
block_button = tk.Button(root, text="Block Domain", command=block_domain, **button_style, cursor="hand2")
block_button.pack(pady=10)

unblock_button = tk.Button(root, text="Unblock Domain", command=unblock_domain, **button_style, cursor="hand2")
unblock_button.pack(pady=10)

# Dark/Light mode toggle button
toggle_button = tk.Button(root, text="Toggle Dark/Light Mode", command=toggle_theme, **button_style, cursor="hand2")
toggle_button.pack(pady=20)

# Set the initial theme
set_theme(light_theme_colors)

# Start the GUI loop
root.mainloop()
