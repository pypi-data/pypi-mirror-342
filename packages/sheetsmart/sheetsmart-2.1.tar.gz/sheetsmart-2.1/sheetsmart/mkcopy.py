import os
import shutil
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
def mkcopy():
    src_filename = input("Enter the filename to copy:").lower() + ".csv"
    src_filepath = os.path.join("data", src_filename)
    
    if not os.path.exists(src_filepath):
        print("Error: Source file does not exist! Check your filename and try again.")
        return
    
    # Determine the destination directory based on OS
    if os.name == 'nt':  # Windows
        dest_dir = os.path.join(os.getenv('USERPROFILE'), 'Downloads', 'SheetSmart Data')
    else:  # macOS and Linux
        dest_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'SheetSmart Data')
    
    os.makedirs(dest_dir, exist_ok=True)  # Create directory if it doesn't exist
    
    copy_filepath = os.path.join(dest_dir, src_filename)
    shutil.copy2(src_filepath, copy_filepath)  # Copy file
    
    print(f"File has been copied successfully to: {copy_filepath}")
    print("From here, you can now share your file anywhere on the internet or across devices.")

