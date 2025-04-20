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
def write():
    os.makedirs("data", exist_ok=True)
    
    while True:
        filename = input("Enter the filename:").lower() + ".csv"
        filepath = os.path.join("data", filename)
        
        if os.path.exists(filepath):
            choice = input("File already exists. Enter a new name or type 'replace' to overwrite: ").lower()
            if choice == "replace":
                break
            elif choice == "exit":
                print("Operation cancelled.")
                return
            else:
                filename = choice + ".csv"
                filepath = os.path.join("data", filename)
        else:
            print(f"New file '{filename}' will be created.")
            break
    
    column_names = []
    print("Enter column names one by one. Type 'n' or 'exit' to stop adding columns.")
    while True:
        col_name = input("Enter column name: ").lower()
        if col_name in ['n', 'exit']:
            break
        column_names.append(col_name)
    
    with open(filepath, mode='a+', newline='') as file:
        writer = csv.writer(file)
        
        # Move to the start and check if file is empty to write headers
        file.seek(0)
        if file.read().strip() == "":
            writer.writerow(["id"] + column_names)
        
        print("Enter row data. Type 'n' or 'exit' to stop adding rows.")
        i = 0
        while True:
            row_data = []
            for col in column_names:
                value = input(f"Enter data for {col} (Row {i}): ").lower()
                if value in ['n', 'exit']:
                    print(f"CSV file '{filename}' has been updated successfully!")
                    return
                row_data.append(value)
            writer.writerow([i] + row_data)
            i += 1

def read(filename):
    filepath = os.path.join("data", filename.lower() + ".csv")
    if not os.path.exists(filepath):
        print("Error: File does not exist!")
        return
    
    with open(filepath, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
