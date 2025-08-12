import os
import subprocess
import sys

def run_scripts_in_folder(folder_path, url):
    # Path to the virtual environment's Python executable
    venv_python = os.path.join(os.path.dirname(__file__), 'venv', 'Scripts', 'python.exe')
    
    # Check if the virtual environment's Python executable exists
    if not os.path.exists(venv_python):
        raise FileNotFoundError(f"Virtual environment Python executable not found: {venv_python}")
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".py"):
            script_path = os.path.join(folder_path, filename)
            subprocess.run([venv_python, script_path, url], check=True)

if __name__ == "__main__":
    scripts_folder = os.path.join(os.path.dirname(__file__), 'scripts')
    url = sys.argv[1] if len(sys.argv) > 1 else "https://itexamanswers.net/ccna-2-v7-0-final-exam-answers-full-switching-routing-and-wireless-essentials.html"
    if not url:
        raise ValueError("URL argument is required")
    run_scripts_in_folder(scripts_folder, url)