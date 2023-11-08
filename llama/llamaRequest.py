# import requests

# API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-hf"
# headers = {"Authorization": f"Bearer {apiToken}"}

# def query(payload):
# 	response = requests.post(API_URL, headers=headers, json=payload)
# 	return response.json()
	
# output = query({
# 	"inputs": "Can you please let us know more details about your ",
# })

# print(output)



# import json
# import requests
# API_URL = "https://api-inference.huggingface.co/models/gpt2"
# headers = {"Authorization": f"Bearer {apiToken}"}
# def query(payload):
#     data = json.dumps(payload)
#     response = requests.request("POST", API_URL, headers=headers, data=data)
#     return json.loads(response.content.decode("utf-8"))
# data = query("hello how are you ")
# print(data)


# huggingface-cli login

# make sure to download model file to d drive
import os
os.environ['TRANSFORMERS_CACHE'] = 'D:/huggingface'



from transformers import AutoTokenizer
import transformers
import torch
model = "meta-llama/Llama-2-7b-chat-hf"



tokenizer = AutoTokenizer.from_pretrained(model, use_auth_token=True, use_flash_attention_2=True)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device_map="auto",
)

sequences = pipeline(
    'Do you know how to write python codeS?\n',
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    max_length=200,
)
for seq in sequences:
    print(f"Result: {seq['generated_text']}")


