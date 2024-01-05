import os

def get_folder_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size

def find_subfolders_sorted_by_size(path):
    folder_sizes = []

    for dirpath, dirnames, filenames in os.walk(path):
        folder_size = get_folder_size(dirpath)
        folder_sizes.append((dirpath, folder_size))

    # Sort the list of tuples by folder size in descending order
    sorted_folders = sorted(folder_sizes, key=lambda x: x[1], reverse=True)

    return sorted_folders

if __name__ == "__main__":
    folder_path = input("Enter the path to the directory: ")

    if os.path.exists(folder_path):
        sorted_folders = find_subfolders_sorted_by_size(folder_path)
        print("Subfolders ranked by size:")
        for folder, size in sorted_folders:
            print(f"Folder: '{folder}' - Size: {size} bytes")
    else:
        print("The specified directory does not exist.")
