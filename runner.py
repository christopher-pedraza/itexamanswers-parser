import os
import subprocess

def run_scripts_in_folder(folder_path):
    # Path to the virtual environment's Python executable
    venv_python = os.path.join(os.path.dirname(__file__), 'venv', 'Scripts', 'python.exe')
    
    # Check if the virtual environment's Python executable exists
    if not os.path.exists(venv_python):
        raise FileNotFoundError(f"Virtual environment Python executable not found: {venv_python}")
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".py"):
            script_path = os.path.join(folder_path, filename)
            subprocess.run([venv_python, script_path], check=True)

if __name__ == "__main__":
    scripts_folder = os.path.join(os.path.dirname(__file__), 'scripts')
    run_scripts_in_folder(scripts_folder)