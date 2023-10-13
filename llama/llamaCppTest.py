from llama_cpp import Llama

llm = Llama(model_path="D:/AI/llama.cpp/models/7B/ggml-model-q4_0.gguf")

# chatgpt like api works
output = llm("Q: Name the planets in the solar system? A: ", max_tokens=32, stop=["Q:", "\n"], echo=True)
print(output)

