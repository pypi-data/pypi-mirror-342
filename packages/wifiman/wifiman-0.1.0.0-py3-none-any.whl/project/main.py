# Copyright (c) 2025 Krishnakanth Allika, richly-human-grew@duck.com
# Licensed under the GNU General Public License v3 (GPLv3).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see https://www.gnu.org/licenses/gpl-3.0-standalone.html
#

"""
Windows WiFi Manager (WiFiMan)

A simple GUI application for managing WiFi connections on Windows systems.
This tool provides the following functionality:
- Automatic WiFi troubleshooting (disabling/enabling adapter when connectivity is lost)
- Listing available WiFi profiles on the system
- Easy connection to saved WiFi networks
- Detailed color-coded logging of network operations

The interface features a dark mode design with intuitive controls for common
WiFi management tasks. Compatible with Windows 10 and Windows 11.

Usage:
- Click "Troubleshoot Wi-Fi" to automatically repair a broken connection
- Click "List Wi-Fi" to populate the dropdown with available network profiles
- Select a profile and click "Connect" to connect to that network

All operations are logged in the console window with color-coded message types.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import threading
import time
import webbrowser


def run_command(command):
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
        )
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)


def get_wifi_interface_name():
    # Get list of network interfaces
    output = run_command("netsh interface show interface")
    for line in output.splitlines():
        # Look for enabled wireless interfaces
        if "Wireless" in line and "Enabled" in line:
            parts = line.split()
            # Interface name is usually the last part
            if len(parts) >= 4:
                return parts[-1]
    # Fallback to common names if can't find
    return "Wi-Fi"  # Common name, might be "Wireless Network Connection" or others


def log_output(text, message_type="INFO"):
    """
    Add colored text to the log area based on message type.
    message_type can be: "INFO", "SUCCESS", "ERROR", "WARNING", "COMMAND", "DEBUG"
    """
    log_area.configure(state="normal")

    # Define colors for different message types
    colors = {
        "INFO": "#FFFFFF",  # White
        "SUCCESS": "#4CAF50",  # Green
        "ERROR": "#F44336",  # Red
        "WARNING": "#FFC107",  # Amber/Yellow
        "COMMAND": "#2196F3",  # Blue
        "DEBUG": "#9C27B0",  # Purple
        "SYSTEM": "#607D8B",  # Blue Gray
    }

    # Add timestamps to logs
    timestamp = time.strftime("[%H:%M:%S] ", time.localtime())
    prefix_map = {
        "INFO": "[INFO] ",
        "SUCCESS": "[SUCCESS] ",
        "ERROR": "[ERROR] ",
        "WARNING": "[WARNING] ",
        "COMMAND": "[COMMAND] ",
        "DEBUG": "[DEBUG] ",
        "SYSTEM": "[SYSTEM] ",
    }

    prefix = prefix_map.get(message_type, "")
    formatted_text = timestamp + prefix + text

    # Define a tag specifically for this message type
    color = colors.get(message_type, "#FFFFFF")
    tag_name = f"color_{message_type}"  # Fixed: added closing brace

    # Configure the tag with the appropriate color
    log_area.tag_configure(tag_name, foreground=color)

    # Insert the text with the tag applied
    log_area.insert(tk.END, formatted_text, tag_name)

    log_area.see(tk.END)
    log_area.configure(state="disabled")


def reset_wifi():
    def task():
        log_output("Starting Wi-Fi troubleshooting process\n", "INFO")
        interface_name = get_wifi_interface_name()
        log_output(f"Using network interface: '{interface_name}'\n", "SYSTEM")
        log_output("Beginning connection test...\n", "INFO")

        while True:
            log_output("Testing internet connectivity with ping...\n", "DEBUG")
            result = subprocess.run(
                "ping -n 1 www.google.com",
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=True,
            )
            if result.returncode != 0:
                log_output("⚠️ Internet connection lost!\n", "ERROR")
                log_output(
                    "Detailed diagnosis: Cannot reach google.com (ping failed)\n",
                    "DEBUG",
                )
                log_output("Attempting connection recovery procedure...\n", "INFO")

                log_output("STEP 1/3: Disabling Wi-Fi adapter...\n", "WARNING")
                disable_command = f'netsh interface set interface name="{interface_name}" admin=disabled'
                log_output(f"Executing: {disable_command}\n", "DEBUG")
                disable_output = run_command(disable_command)
                log_output(f"System response: {disable_output}\n", "COMMAND")

                log_output("Waiting 5 seconds for hardware reset...\n", "SYSTEM")
                time.sleep(5)

                log_output("STEP 2/3: Enabling Wi-Fi adapter...\n", "WARNING")
                enable_command = f'netsh interface set interface name="{interface_name}" admin=enabled'
                log_output(f"Executing: {enable_command}\n", "DEBUG")
                enable_output = run_command(enable_command)
                log_output(f"System response: {enable_output}\n", "COMMAND")

                log_output(
                    "STEP 3/3: Waiting for network reconnection (30s)...\n", "WARNING"
                )
                for i in range(6):
                    log_output(
                        f"Reconnection in progress... ({(i+1)*5}s of 30s)\n", "SYSTEM"
                    )
                    time.sleep(5)
                log_output("Wait complete, testing connection again...\n", "INFO")
            else:
                log_output("✅ Internet connection successfully verified!\n", "SUCCESS")
                log_output("Connection troubleshooting complete\n", "INFO")
                break

    threading.Thread(target=task, daemon=True).start()


def list_wifi_profiles():
    log_output("Retrieving available Wi-Fi profiles...\n", "INFO")
    command = "netsh wlan show profiles"
    log_output(f"Executing: {command}\n", "DEBUG")
    output = run_command(command)

    profiles = []
    for line in output.splitlines():
        if "All User Profile" in line:
            profile = line.split(":")[1].strip()
            profiles.append(profile)

    if not profiles:
        log_output("No Wi-Fi profiles found on this system\n", "ERROR")
        log_output("Please create at least one Wi-Fi profile first\n", "INFO")
        return

    log_output(f"Found {len(profiles)} Wi-Fi profiles:\n", "INFO")
    for i, profile in enumerate(profiles):
        log_output(f"  {i+1}. {profile}\n", "SYSTEM")

    wifi_dropdown["values"] = profiles
    if profiles:
        wifi_dropdown.set(profiles[0])
        log_output(f"Selected '{profiles[0]}' as default profile\n", "INFO")

    log_output("Wi-Fi profiles loaded successfully\n", "SUCCESS")


def connect_to_wifi():
    selected_wifi = wifi_var.get()
    if not selected_wifi:
        log_output("Error: No Wi-Fi profile selected\n", "ERROR")
        log_output("Please select a Wi-Fi profile from the dropdown list\n", "INFO")
        return

    log_output(f"Initiating connection to '{selected_wifi}'...\n", "WARNING")
    command = f'netsh wlan connect interface="Wi-Fi" name="{selected_wifi}"'
    log_output(f"Executing: {command}\n", "DEBUG")
    output = run_command(command)

    if "Connection request was completed successfully" in output:
        log_output(f"✅ Successfully connected to {selected_wifi}\n", "SUCCESS")
    elif "already connected" in output.lower():
        log_output(f"Already connected to {selected_wifi}\n", "INFO")
    else:
        log_output(f"⚠️ Connection attempt returned: {output}\n", "COMMAND")
        log_output(
            "Please check that the profile exists and Wi-Fi is enabled\n", "ERROR"
        )


def open_link(event):
    webbrowser.open("https://go.allika.eu.org/wifiman")


# GUI Setup
app = tk.Tk()
app.title("Allika's Simple Windows WiFi Manager")
app.geometry("600x430")  # Increased height for footer

# Set up dark mode
app.configure(bg="#2E2E2E")
style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#2E2E2E")

# Common orange button style with black text
ORANGE_COLOR = "#FF5722"
ORANGE_ACTIVE = "#E64A19"

style.configure(
    "TButton",
    background=ORANGE_COLOR,
    foreground="black",  # Changed from "white" to "black"
    borderwidth=1,
    focusthickness=3,
    focuscolor="none",
)
style.map("TButton", background=[("active", ORANGE_ACTIVE)])
style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF")
style.configure(
    "TCombobox", fieldbackground="#3E3E3E", background="#5E5E5E", foreground="#FFFFFF"
)

frame = ttk.Frame(app, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

# Line 1: Troubleshoot Wi-Fi button with Windows compatibility info
button_info_frame = ttk.Frame(frame)
button_info_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

# Troubleshoot button on the left
reset_btn = ttk.Button(button_info_frame, text="Troubleshoot Wi-Fi", command=reset_wifi)
reset_btn.pack(side=tk.LEFT)

# "Tested on..." text on the right
compatibility_label = ttk.Label(
    button_info_frame,
    text="Tested on Windows 10 & 11",
    foreground="#FFFFFF",
    font=("Arial", 8, "italic"),
)
compatibility_label.pack(side=tk.RIGHT)

# Line 2: List Wi-Fi button (already left-aligned)
list_btn = ttk.Button(frame, text="List Wi-Fi", command=list_wifi_profiles)
list_btn.grid(
    row=1, column=0, padx=5, pady=5, sticky="w"
)  # Added sticky="w" for left alignment

# Dropdown for Wi-Fi selection
wifi_var = tk.StringVar()
wifi_dropdown = ttk.Combobox(frame, textvariable=wifi_var, width=40)
wifi_dropdown.grid(row=1, column=1, pady=10, padx=5, sticky="ew")

# Connect button - moved to left alignment
connect_btn = ttk.Button(frame, text="Connect", command=connect_to_wifi)
connect_btn.grid(
    row=1, column=2, padx=5, pady=10, sticky="w"
)  # Added sticky="w" for left alignment

# Log area - changed background to full black (#000000)
log_area = scrolledtext.ScrolledText(
    frame,
    wrap=tk.WORD,
    state="disabled",
    height=15,
    bg="#000000",  # Changed from #3E3E3E to #000000 (full black)
    fg="#FFFFFF",
    insertbackground="#FFFFFF",
)
log_area.grid(row=2, column=0, columnspan=3, pady=10, sticky="nsew")

frame.rowconfigure(2, weight=1)
frame.columnconfigure(1, weight=1)  # Make the middle column (with dropdown) expandable

# Footer with clickable link - properly centered
footer_frame = ttk.Frame(app, style="Footer.TFrame")
style.configure("Footer.TFrame", background="#1E1E1E")
footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=5)

footer_text = "(c) 2025 Krishnakanth Allika"
link_text = "https://go.allika.eu.org/wifiman"

# Configure footer text style
style.configure(
    "Footer.TLabel", background="#1E1E1E", foreground=ORANGE_COLOR, font=("Arial", 8)
)

# Create a container frame to hold both labels
container_frame = ttk.Frame(footer_frame, style="Footer.TFrame")
container_frame.pack(side=tk.TOP)

# Footer copyright text
footer_label = ttk.Label(container_frame, text=footer_text, style="Footer.TLabel")
footer_label.pack(side=tk.LEFT)

# Create clickable link label
link_label = tk.Label(
    container_frame,
    text=link_text,
    fg=ORANGE_COLOR,
    bg="#1E1E1E",
    cursor="hand2",
    font=("Arial", 8),
)
link_label.pack(side=tk.LEFT, padx=(5, 0))
link_label.bind("<Button-1>", open_link)

# Center the container frame in the footer
container_frame.pack(anchor=tk.CENTER)

app.mainloop()
