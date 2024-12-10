import os, sys
import subprocess

def setup_environment():
    os.makedirs("example/default_savepath", exist_ok=True)
    os.makedirs("example/default_search", exist_ok=True)
    user_os=sys.platform

    if user_os=="win32":
        subprocess.run("python -m venv venv", shell=True)
        subprocess.run("venv\\Scripts\\activate && pip install -r requirements.txt && python pyxl_start.py", shell=True)

    elif user_os=="linux":
        subprocess.run("python3 -m venv venv", shell=True)
        subprocess.run("source venv/bin/activate && pip3 install -r requirements.txt && python3 pyxl_start.py", shell=True)

    else:
        print("Operational System not recognized, please check the docs and configure the application first use manually")

if __name__ == "__main__":
    setup_environment()
