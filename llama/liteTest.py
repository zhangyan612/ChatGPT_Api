import os 
from litellm import completion 

# Get the value of the environment variable

print(os.environ['HUGGINGFACE_API_KEY'])

messages = [{ "content": "There's a llama in my garden 😱 What should I do?","role": "user"}]

# e.g. Call 'WizardLM/WizardCoder-Python-34B-V1.0' hosted on HF Inference endpoints
response = completion(
  model="huggingface/WizardLM/WizardCoder-Python-34B-V1.0", 
  messages=messages, 
  api_base="https://my-endpoint.huggingface.cloud"
)

print(response)



# from litellm import completion 

# model = "gpt-3.5-turbo"
# messages = [{"role":"user", "content":"This is a test request"}]

# response =completion(model=model, messages=messages, mock_response="It's simple to use and easy to get started")
# print(response)
