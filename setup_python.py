#!/usr/bin/env python3
"""
Setup script for Python environment for Dr. D's Data Science blog
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages from requirements.txt"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Successfully installed Python requirements!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def check_quarto():
    """Check if Quarto is available"""
    try:
        result = subprocess.run(["quarto", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Quarto is available: {result.stdout.strip()}")
            return True
        else:
            print("❌ Quarto is not available or not in PATH")
            return False
    except FileNotFoundError:
        print("❌ Quarto is not installed")
        return False

def main():
    print("🐍 Setting up Python environment for Dr. D's Data Science...")
    
    # Check if we're in the right directory
    if not os.path.exists("_quarto.yml"):
        print("❌ Please run this script from the root of your Quarto project")
        sys.exit(1)
    
    # Install Python requirements
    if not install_requirements():
        sys.exit(1)
    
    # Check Quarto availability
    check_quarto()
    
    print("\n🎉 Setup complete! You can now use Python in your Quarto documents.")
    print("\nTo render your site with Python support:")
    print("  quarto render")
    print("\nTo preview your site:")
    print("  quarto preview")

if __name__ == "__main__":
    main()
