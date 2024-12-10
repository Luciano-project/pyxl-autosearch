import os, sys
import subprocess

def setup_environment():
    os.makedirs("example/default_savepath", exist_ok=True)
    os.makedirs("example/default_search", exist_ok=True)
    if not os.path.isdir("venv"):
        subprocess.run("python -m venv venv", shell=True)
    
    if sys.platform == "win32":
        subprocess.run("venv/Scripts/activate && pip install -r requirements.txt && python pyxl_start.py", shell=True)
        
    else:
        subprocess.run("source venv/bin/activate && pip install -r requirements.txt && python pyxl_start.py", shell=True)

if __name__ == "__main__":
    setup_environment()
