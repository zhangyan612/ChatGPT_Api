import subprocess

# Replace 'your_application.exe' with the path to the Windows application you want to run.
app_path = r'C:\path\to\your_application.exe'

try:
    # Use the subprocess.Popen function to start the application.
    subprocess.Popen(app_path)
    print(f"Started {app_path}")
except FileNotFoundError:
    print(f"Error: {app_path} not found.")
except Exception as e:
    print(f"An error occurred: {e}")
