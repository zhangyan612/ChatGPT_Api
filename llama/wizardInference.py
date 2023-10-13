import json
import requests
import os

API_TOKEN = os.environ['HUGGINGFACE_API_KEY']

# headers = {"Authorization": f"Bearer {API_TOKEN}"}
# API_URL = "https://api-inference.huggingface.co/models/WizardLM/WizardCoder-Python-34B-V1.0"
# def query(payload):
#     data = json.dumps(payload)
#     response = requests.request("POST", API_URL, headers=headers, data=data)
#     return json.loads(response.content.decode("utf-8"))
# data = query({"inputs": "Can you write python code? ."})
# print(data)

# Need huggingface pro account

import json
import requests
headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/bert-base-uncased"
def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))
data = query({"inputs": "The answer to the universe is [MASK]."})
print(data)


#require hugging face pro subscription