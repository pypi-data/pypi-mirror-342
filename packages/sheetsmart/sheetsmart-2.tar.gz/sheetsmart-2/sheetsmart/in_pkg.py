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

# Call the function
in_pkg()

