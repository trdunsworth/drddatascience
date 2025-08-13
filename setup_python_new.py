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
            "ipykernel", "python-dotenv", "requests", "plotly", "altair",
            "tsfresh", "sktime", "mapie", "pyarrow",
            "statsforecast", "neuralforecast", "nixtla", "hierarchicalforecast",
            "mlforecast", "tsfeatures", "polars", "duckdb", "whenever"
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
            return True
        else:
            print("❌ Quarto is not available or not in PATH")
            return False
    except FileNotFoundError:
        print("❌ Quarto is not installed")
        print("💡 Install Quarto from: https://quarto.org/docs/get-started/")
        return False

def test_python_execution():
    """Test that Python execution works with Quarto"""
    print("🧪 Testing Python execution with Quarto...")
    
    # Create a simple test file
    test_content = """---
title: "Python Test"
execute: 
  eval: true
---

```{python}
print("Python is working in Quarto!")
import pandas as pd
print(f"Pandas version: {pd.__version__}")
```
"""
    
    with open("test_python_setup.qmd", "w") as f:
        f.write(test_content)
    
    try:
        # Activate environment and render
        result = subprocess.run([
            "bash", "-c", 
            "source .venv/bin/activate && quarto render test_python_setup.qmd"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Python execution test passed!")
            # Clean up
            os.remove("test_python_setup.qmd")
            if os.path.exists("_site/test_python_setup.html"):
                os.remove("_site/test_python_setup.html")
            return True
        else:
            print("❌ Python execution test failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error during Python test: {e}")
        return False

def main():
    print("🚀 Setting up Python environment for Dr. D's Data Science with uv...")
    
    # Check if we're in the right directory
    if not os.path.exists("_quarto.yml"):
        print("❌ Please run this script from the root of your Quarto project")
        sys.exit(1)
    
    # Check uv availability
    if not check_uv():
        sys.exit(1)
    
    # Create environment and install packages (skip if already exists)
    if os.path.exists(".venv"):
        print("📁 Virtual environment already exists, installing packages...")
        try:
            packages = [
                "pandas", "numpy", "matplotlib", "seaborn", "scipy",
                "statsmodels", "scikit-learn", "sqlalchemy", "pyodbc", 
                "psycopg2-binary", "folium", "geopandas", "jupyter", 
                "ipykernel", "python-dotenv", "requests", "plotly", "altair"
            ]
            subprocess.check_call(["uv", "pip", "install"] + packages)
            print("✅ Packages updated!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error updating packages: {e}")
            sys.exit(1)
    else:
        if not create_venv_and_install():
            sys.exit(1)
    
    # Check Quarto availability
    if not check_quarto():
        print("⚠️  Quarto not found, but Python environment is ready")
    else:
        # Test Python execution
        test_python_execution()
    
    print("\n🎉 Setup complete! Your Python environment is ready.")
    print("\n📋 Usage:")
    print("  # Activate environment and render:")
    print("  source .venv/bin/activate && quarto render")
    print("")
    print("  # Or use the convenience script:")
    print("  ./with_python_env.sh quarto render")
    print("  ./with_python_env.sh quarto preview")
    print("")
    print("📝 To use Python in your posts, create code blocks like:")
    print("```{python}")
    print("#| echo: true")
    print("import pandas as pd")
    print("# Your Python code here")
    print("```")

if __name__ == "__main__":
    main()
