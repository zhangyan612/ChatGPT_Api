import requests


class Completion:
    def __init__(self):
        self.url = 'http://127.0.0.1:5000/chat'
        self.chat_history = []


    def create(self, message, model= 'gpt-3.5-turbo'):
        myobj = {
            'model': model, 
            'messages': message
        }
        x = requests.post(self.url, json = myobj)

        self.chat_history.append({'role': 'user', 'content': message})
        return x.json()

    def get_chat_history(self):
        return self.chat_history



chat = Completion()
response = chat.create('Write a simple react todo app')

print(response['choices'][0]['message']['content'])

