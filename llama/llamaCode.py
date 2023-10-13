import os
os.environ['TRANSFORMERS_CACHE'] = 'D:/huggingface'

from transformers import (
    GenerationConfig,
    PreTrainedTokenizerFast,
    LlamaForCausalLM,
    TextStreamer,
    PreTrainedTokenizerFast
)
import torch

# not working

model_path = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = PreTrainedTokenizerFast(tokenizer_file=model_path+"/tokenizer.json")
model = LlamaForCausalLM.from_pretrained(model_path, low_cpu_mem_usage=True, device_map="auto", torch_dtype=torch.float16, local_files_only=True)

prompt = "What is your opinion about fantasies to avoid the real world."
inputs = tokenizer(prompt, return_tensors="pt")


input_ids = inputs.input_ids.to('cuda')

streamer = TextStreamer(tokenizer)


generation_config = GenerationConfig.from_pretrained(model_path,  "generation_config.json")
print(generation_config)

import time
start = time.time()

_ = model.generate(input_ids, streamer=streamer,generation_config=generation_config)

end = time.time()
print(end - start)
