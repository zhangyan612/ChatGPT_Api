from llama_cpp import Llama

llm = Llama(model_path="D:/AI/llama.cpp/models/7B/ggml-model-q4_0.gguf")

# chatgpt like api works
output = llm("Q: Name the planets in the solar system? A: ", max_tokens=350, stop=["Q:", "\n"], echo=True)
print(output)


# issue not using GPU and it's slow

# D:\ProgramData\miniconda3

# export LLAMA_CPP_LIB=/yourminicondapath/miniconda3/lib/python3.10/site-packages/llama_cpp_cuda/libllama.so
import os
print(os.environ['path'])


