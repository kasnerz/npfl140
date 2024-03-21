#!/usr/bin/env python3

"""
Minimal example of decoding with a pretrained GPT-2 model using the `transformers` library.
"""

from transformers import AutoModelForCausalLM, AutoTokenizer

# usually the namespace/model_name, such as "mistralai/Mistral-7B-v0.1"
# gpt2 is an older model and kind of "default" for many examples, that's why we can use a short name instead of "openai-community/gpt2"
model_name = "gpt2"

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
    do_sample=True,
    top_k=10,
    top_p=0.9,
    num_beams=5,
    num_return_sequences=5
)
output_text = tokenizer.batch_decode(output_ids)

print(output_text)
