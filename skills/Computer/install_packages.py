import subprocess

packages_to_install = [
    "llama-cpp-python",
]

log_file = "pip_install_log.txt"

with open(log_file, "w") as log:
    for package in packages_to_install:
        try:
            subprocess.check_call(["pip", "install", package], stdout=log, stderr=subprocess.STDOUT)
            log.write(f"Successfully installed {package}\n")
        except subprocess.CalledProcessError as e:
            log.write(f"Failed to install {package}: {e}\n")

print(f"Installation log saved to {log_file}")
