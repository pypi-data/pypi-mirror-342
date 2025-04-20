import os
import pandas as pd
import matplotlib.pyplot as plt
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
def bar5():
    os.makedirs("data", exist_ok=True)
    
    filename = input("Enter the filename to analyze (without extension): ").lower() + ".csv"
    filepath = os.path.join("data", filename)
    
    if not os.path.exists(filepath):
        print("Error: File does not exist! Check the name of the file or use sheetsmart.write() to create a table.")
        return
    
    df = pd.read_csv(filepath)
    df.columns = [col.lower() for col in df.columns]  # Convert column names to lowercase
    
    while True:
        column_name = input("Enter the column name to analyze: ").strip().lower()
        
        if column_name in df.columns:
            break
        
        # Suggest a possible correct column name
        suggestions = [col for col in df.columns if column_name in col or col in column_name]
        if suggestions:
            print(f"Error: Column '{column_name}' not found in '{filename}'. You may refer '{suggestions[0]}'?")
        else:
            print(f"Error: Column '{column_name}' not found in '{filename}'. Use sheetsmart.modify() to add a new column.")
            return
    
    plt.figure(figsize=(10, 6))
    plt.hist(df[column_name], bins=5, color='green', edgecolor='white')
    
    plt.xlabel("ID")
    plt.ylabel(column_name.capitalize())
    plt.title(f"Histogram(by SheetSmart) of {column_name.capitalize()}")
    plt.grid(True)
    plt.show()

