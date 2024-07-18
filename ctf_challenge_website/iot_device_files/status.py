#!/usr/bin/env python3

import sys
import os

def check_status(device_name):
    try:
        file_path = os.path.join(os.path.dirname(__file__), f"{device_name}_status.txt")
        with open(file_path, "r") as file:
            status = file.read().strip()
            return status
    except FileNotFoundError:
        return f"{device_name} status not found."

def list_files():
    try:
        files = os.listdir(os.path.dirname(__file__))
        return "\n".join(files)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./status.py <device_name> [additional commands]")
    else:
        device_name = sys.argv[1]
        if device_name.startswith("device"):
            #flag{command-injection}
            print(check_status(device_name))
        else:
            print("Invalid device name.")
        
        if len(sys.argv) > 2:
            additional_commands = sys.argv[2:]
            if additional_commands[0] == "ls":
                print(list_files())
            else:
                print("Only 'ls' command is allowed as an additional command.")
