from llama_cpp import Llama

# chatgpt like api works

llm = Llama(model_path="D:/AI/llama.cpp/models/7B/ggml-model-q4_0.gguf")

output = llm("Q: Name the planets in the solar system? A: ", max_tokens=350, stop=["Q:", "\n"], echo=True)
print(output)

# AVX = 1 | AVX2 = 1 | AVX512 = 0 | AVX512_VBMI = 0 | AVX512_VNNI = 0 | FMA = 1 | NEON = 0 | ARM_FMA = 0 | F16C = 1 | FP16_VA = 0 | WASM_SIMD = 0 | BLAS = 0 | SSE3 = 1 | SSSE3 = 0 | VSX = 0 |

# issue not using GPU and it's slow

# D:\ProgramData\miniconda3

# export LLAMA_CPP_LIB=/yourminicondapath/miniconda3/lib/python3.10/site-packages/llama_cpp_cuda/libllama.so
# import os
# print(os.environ['path'])


# from llama_cpp import GGML_USE_CUBLAS
# print(GGML_USE_CUBLAS)
# DLLAMA_CUBLAS=ON