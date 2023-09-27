from flask import Flask, request, jsonify
import time
from chatgpt_automation import ChatGPT_Client
import os

app = Flask(__name__)
chatgpt = ChatGPT_Client(os.environ.get('OPENAI_UNAME'), os.environ.get('OPENAI_PWD'), False)
print('app is running')

@app.route('/')
def home():
    return 'This is chat api'

# Define a simple route that accepts POST requests
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json  # Assuming the request data is in JSON format
    
    answer, code = chatgpt.interact(data['messages'])
    result = {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": answer,
                    "code": code,
                    "role": "assistant"
                }
            }
        ],
        "created": int(time.time()),
        "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
        "model": data['model'],
        "object": "chat.completion",

    }
    # Return a JSON response
    return jsonify(result)

if __name__ == '__main__':
    app.run()
