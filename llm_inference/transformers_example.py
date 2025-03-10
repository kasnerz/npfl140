#!/usr/bin/env python3

"""
Minimal example of decoding with a pretrained meta-llama/Llama-3.2-1B model using the `transformers` library.
"""

from transformers import AutoModelForCausalLM, AutoTokenizer

# usually the namespace/model_name, such as "mistralai/Mistral-7B-v0.1"
# model_name = "meta-llama/Llama-3.2-1B-Instruct"
model_name = "meta-llama/Llama-3.2-1B-Instruct"

# prefix given to the model
text = "I am the"

# GPU, use "cpu" for CPU
device = "cuda"

model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# "pt" means pytorch
input_ids = tokenizer(text, return_tensors="pt").to(device)

# all the parameters except input_ids are optional
output_ids = model.generate(
    **input_ids,
    max_new_tokens=5,
    do_sample=False,
    # top_k=10,
    # top_p=0.9,
    num_beams=10,
    num_return_sequences=10
)
output_text = tokenizer.batch_decode(output_ids, skip_special_tokens=True)

breakpoint()
print(output_text)
