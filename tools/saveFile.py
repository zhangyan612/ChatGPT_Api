import json

# save gpt response to response folder
def saveFile(folder, fileName, data):
    file_path = folder + "/" + fileName+ ".json"
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)
    print(f"JSON data has been saved to {file_path}")
