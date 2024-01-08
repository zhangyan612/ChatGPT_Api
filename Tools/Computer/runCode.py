import subprocess
import threading

def runCode(codeType, script_path):
    try:
        # Run the script and capture its output
        result = subprocess.run([codeType, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        
        # Process the output
        output = result.stdout
        error_output = result.stderr
        
        # Do something with the output, e.g., print it
        print("Output:\n", output)
        
        if error_output:
            print("Error Output:\n", error_output)
    except subprocess.CalledProcessError as e:
        print(f"Error running the script: {e}")
    except FileNotFoundError:
        print(f"Script '{script_path}' not found.")



if __name__ == "__main__":
    # Define the path to the script you want to execute

    codeType = "python"
    script_path = "codeRunner/testCode.py"

    # Create a separate thread to execute the script
    script_thread = threading.Thread(target=runCode, args=(codeType, script_path,))

    # Start the thread
    script_thread.start()

    # Optionally, you can wait for the thread to finish
    # script_thread.join()

    # Continue with other tasks here while the script is running in the background
    print("Main thread continues to run...")
