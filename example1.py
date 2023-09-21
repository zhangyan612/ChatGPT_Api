from chatgpt_automation import ChatGPT_Client
import os

chatgpt = ChatGPT_Client(os.environ.get('OPENAI_UNAME'), os.environ.get('OPENAI_PWD'))

answer = chatgpt.interact("Hello, Can you write python code")

print(answer)
