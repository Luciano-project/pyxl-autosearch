import os, sys
import subprocess
import time

def setup_environment():
    user_os=sys.platform
    command = {"linux": {"create_env": "python3 -m venv venv",
                         "active_venv": "venv/bin/activate",
                         "install_requirements": "pip install -r requirements.txt",
                         "create_example": "venv/bin/python3 pyxl_start.py",
                         },

                "windows":{"create_env": "python -m venv venv",
                         "active_venv": "venv\\Scripts\\activate",
                         "install_requirements": "pip install -r requirements.txt",
                         "create_example": "python pyxl_start.py",
                         }
                }


    os.makedirs("example/default_savepath", exist_ok=True)
    os.makedirs("example/default_search", exist_ok=True)
    try:
        if user_os=="win32":
            cmd_os = command['windows']
            subprocess.run(f"{cmd_os['create_env']} && {cmd_os['active_venv']} && {cmd_os['install_requirements']} && {cmd_os['create_example'] }", shell=True)

        elif user_os=="linux":
            cmd_os = command['linux']
            subprocess.run(f"{cmd_os['create_env']}", shell=True)
            subprocess.run(f" bash -c 'source {cmd_os['active_venv']} && {cmd_os['install_requirements']}' && {cmd_os['create_example'] }", shell=True, check=True)
            subprocess.run(f" bash -c 'source {cmd_os['active_venv']} && {cmd_os['create_example']}'", shell=True, check=True)
        else:
            print("Operational System not recognized, please check the docs and configure the application for first use manually")

    except Exception as e: print("error:", e)

if __name__ == "__main__":
    setup_environment()
