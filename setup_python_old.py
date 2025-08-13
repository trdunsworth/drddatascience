#!/usr/bin/env python3
"""
Setup script for Python environment for Dr. D's Data Science blog using uv
"""

import subprocess
import sys
import os

def check_uv():
    """Check if uv is available"""
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ uv is available: {result.stdout.strip()}")
            return True
        else:
            print("❌ uv is not available or not in PATH")
            return False
    except FileNotFoundError:
        print("❌ uv is not installed")
        print("💡 Install uv from: https://docs.astral.sh/uv/getting-started/installation/")
        return False

def create_venv_and_install():
    """Create virtual environment and install packages using uv"""
    try:
        # Create virtual environment
        print("🐍 Creating virtual environment with uv...")
        subprocess.check_call(["uv", "venv"])
        print("✅ Virtual environment created!")
        
        # Install packages
        print("📦 Installing Python packages...")
        packages = [
            "pandas", "numpy", "matplotlib", "seaborn", "scipy",
            "statsmodels", "scikit-learn", "sqlalchemy", "pyodbc", 
            "psycopg2-binary", "folium", "geopandas", "jupyter", 
            "ipykernel", "python-dotenv", "requests", "plotly", "altair"
        ]
        
        subprocess.check_call(["uv", "pip", "install"] + packages)
        print("✅ Successfully installed Python packages!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during setup: {e}")
        return False

def check_quarto():
    """Check if Quarto is available and can detect Python"""
    try:
        result = subprocess.run(["quarto", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Quarto is available: {result.stdout.strip()}")
            
            # Check if Quarto can detect Jupyter
            print("🔍 Checking Quarto Python integration...")
            jupyter_check = subprocess.run(["quarto", "check", "jupyter"], 
                                         capture_output=True, text=True)
            if jupyter_check.returncode == 0:
                print("✅ Quarto can detect Python and Jupyter!")
                return True
            else:
                print("⚠️  Quarto detected but may have issues with Python integration")
                print("💡 Try activating the environment: source .venv/bin/activate")
                return False
        else:
            print("❌ Quarto is not available or not in PATH")
            return False
    except FileNotFoundError:
        print("❌ Quarto is not installed")
        print("💡 Install Quarto from: https://quarto.org/docs/get-started/")
        return False

def main():
    print("� Setting up Python environment for Dr. D's Data Science with uv...")
    
    # Check if we're in the right directory
    if not os.path.exists("_quarto.yml"):
        print("❌ Please run this script from the root of your Quarto project")
        sys.exit(1)
    
    # Check uv availability
    if not check_uv():
        sys.exit(1)
    
    # Create environment and install packages
    if not create_venv_and_install():
        sys.exit(1)
    
    # Check Quarto availability
    check_quarto()
    
    print("\n🎉 Setup complete! You can now use Python in your Quarto documents.")
    print("\n📋 Next steps:")
    print("  1. Activate the environment: source .venv/bin/activate")
    print("  2. Render your site: quarto render")
    print("  3. Preview your site: quarto preview")
    print("\n💡 The environment will be automatically activated when using:")
    print("     uv run quarto render")
    print("     uv run quarto preview")

if __name__ == "__main__":
    main()
