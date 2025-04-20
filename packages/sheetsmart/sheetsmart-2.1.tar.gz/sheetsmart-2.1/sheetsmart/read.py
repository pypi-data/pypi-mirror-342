import csv
import os
import subprocess
import sys
import importlib.util

def is_installed(package_name):
    return importlib.util.find_spec(package_name) is not None

def in_pkg():
    def install_if_missing(package_name):
        if not is_installed(package_name):
            print(f"📦 Installing {package_name}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
                print(f"""
✅ You're using **Sheetsmart** — a powerful tool for data manipulation using Python!
📊 It makes working with data easier and shareable.
🛠️ Developed by Bhuvanesh M.
                """)
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package_name}")
        else:
            print(f"✅ {package_name} is already installed. Skipping installation.")

    for package in ["numpy", "pandas"]:
        install_if_missing(package)
in_pkg()
def read():
    os.makedirs("data", exist_ok=True)
    
    while True:
        filename = input("Enter the filename to read:").lower() + ".csv"
        filepath = os.path.join("data", filename)
        
        if not os.path.exists(filepath):
            user_input = input("Error: File does not exist! Enter a new filename or type 'exit' to cancel: ").lower()
            if user_input in ['exit', 'n']:
                return
            else:
                filename = user_input + ".csv"
                filepath = os.path.join("data", filename)
                continue
        
        with open(filepath, mode='r', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)
            
            if not data:
                print("Error: File is empty!")
                return
            
            while True:
                print("Do you want to read the full file or a particular row?")
                print("1. Read full file")
                print("2. Read a particular row by ID")
                print("3. Exit")
                choice = input("Enter choice (1/2/3): ").strip()
                
                if choice == '1':
                    for row in data:
                        print(row)
                elif choice == '2':
                    while True:
                        try:
                            row_id = int(input("Enter the row ID to read: "))
                            if 0 <= row_id < len(data):
                                print(data[row_id])
                            else:
                                print("Error: Invalid row ID!")
                        except ValueError:
                            print("Error: Please enter a valid integer ID!")
                        
                        next_action = input("Do you want to read another row? (y/n): ").lower()
                        if next_action != 'y':
                            break
                elif choice == '3' or choice.lower() in ['exit', 'n']:
                    return
                else:
                    print("Invalid choice! Please enter 1, 2, or 3.")

