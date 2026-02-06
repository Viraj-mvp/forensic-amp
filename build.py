import os
import subprocess
import sys

def build():
    # Define the PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=ForensicAmp",
        "--windowed",  # No console window
        "--onefile",   # Single executable
        "--icon=ui/app_icon.ico", # Application Icon
        "--add-data=ui/themes/y2k.qss;ui/themes", # Add theme file
        "--add-data=ui/logo_transparent.png;ui",  # Add logo file (used in UI header)
        "--add-data=ui/logo_icon.png;ui",          # Add window icon file
        "--exclude-module=PyQt6",
        "--exclude-module=PyQt5",
        "--clean",
        "main.py"
    ]

    print("Running PyInstaller...")
    print(" ".join(cmd))
    
    try:
        subprocess.check_call(cmd)
        print("\nBuild successful! Executable is in the 'dist' folder.")
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if pyinstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    build()
