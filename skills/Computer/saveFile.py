import json

# save gpt response to response folder
def saveFile(folder, fileName, data):
    file_path = folder + "/" + fileName+ ".json"
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)
    print(f"JSON data has been saved to {file_path}")


def saveCode(code, fileName):
    with open(fileName, "w") as python_file:
        python_file.write(code)


if __name__ =='__main__':
 
    import json

# Load the JSON file
    json_file_path = "responses/1695795946.json"

    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)
            text_to_save = data['choices'][0]['message']['code'][1]

        if text_to_save:
            # Define the Python file name and extension
            python_file_name = "responses/output.py"

            # Create or overwrite the Python file
            saveCode(text_to_save, python_file_name)

            print(f"Text has been saved to {python_file_name}")
        else:
            print("No text found in the JSON file.")

    except FileNotFoundError:
        print(f"JSON file not found: {json_file_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
