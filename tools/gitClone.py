import subprocess

def gitClone(repoUrl, name):
    destination_directory = '/repos/' + name
    try:
        # Run the 'git clone' command using subprocess
        subprocess.run(['git', 'clone', repoUrl, destination_directory], check=True)
        print(f"Repository cloned successfully to {destination_directory}")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")

if __name__ == '__main__':
    gitClone("https://github.com/zhangyan612/RoboCore.git", "RoboCore")