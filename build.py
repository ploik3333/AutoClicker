import subprocess, sys

# subprocess.run(["dir"])
# subprocess.run([sys.executable, "-m", "pip", "list"])
subprocess.run(["pyinstaller", "main.spec", "-y"])