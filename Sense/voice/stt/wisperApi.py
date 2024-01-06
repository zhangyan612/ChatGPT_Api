import requests
import os

#working 
apiKey = os.environ['HUGGINGFACE_API_KEY']

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v2"
headers = {"Authorization": f"Bearer {apiKey}"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()



result = query("D:/Download/sample1.flac")
print(result)