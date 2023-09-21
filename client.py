import requests
import json

# save gpt response to response folder
def saveFile(fileName, data):
    file_path = "responses/" + fileName+ ".json"
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)
    print(f"JSON data has been saved to {file_path}")


class Completion:
    def __init__(self):
        self.url = 'http://127.0.0.1:5000/chat'
        self.chat_history = []


    def create(self, message, model= 'gpt-3.5-turbo'):
        myobj = {
            'model': model, 
            'messages': message
        }
        response = requests.post(self.url, json = myobj)

        self.chat_history.append({'role': 'user', 'content': message})
        return response.json()

    def get_chat_history(self):
        return self.chat_history



chat = Completion()
response = chat.create('are you human?')

print(response['choices'][0]['message']['content'])
saveFile(str(response["created"]), response)