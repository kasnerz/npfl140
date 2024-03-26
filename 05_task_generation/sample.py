#!/usr/bin/env python3

import os
import requests
import argparse
import json

API_KEY = "npfl140"


def load_data(task, split):
    # load all the JSON files in the `data/task/split` directory
    # return a list of dictionaries
    data = []

    for filename in sorted(os.listdir(f"data/{task}/{split}")):
        with open(f"data/{task}/{split}/{filename}") as f:
            data.append(json.load(f))

    return data


def base_model_api(node, model_args, prompt):
    API_URL = (
        f"http://quest.ms.mff.cuni.cz/nlg/text-generation-api-node{node}/v1/completions"
    )
    data = {"prompt": prompt, **model_args}

    response = requests.post(
        API_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        json=data,
        verify=False,
    )
    output_text = response.json()["choices"][0]["text"]

    return output_text


def instruct_model_api(node, model_args, prompt):
    API_URL = f"http://quest.ms.mff.cuni.cz/nlg/text-generation-api-node{node}/v1/chat/completions"

    messages = [{"role": "user", "content": prompt}]
    data = {"mode": "instruct", "messages": messages, **model_args}

    response = requests.post(
        API_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        json=data,
        verify=False,
    )
    breakpoint()
    output_text = response.json()["choices"][0]["message"]["content"]

    return output_text


if __name__ == "__main__":
    # fmt: off
    parser = argparse.ArgumentParser()
    parser.add_argument("--node", "-n", help="Node number (see the instructions for details)", type=int, required=True) 
    parser.add_argument("--max_tokens", "-m", help="Maximum number of tokens to generate", type=int, default=300) 
    parser.add_argument("--seed", "-r", help="Seed for random number generator", type=int, default=42) 
    parser.add_argument("--temperature", "-t", help="Temperature parameter", type=float, default=1.0) 
    parser.add_argument("--top_p", "-p", help="Top-p sampling parameter", type=float, default=1.0) 
    parser.add_argument("--top_k", "-k", help="Top-k sampling parameter", type=int, default=0)
    parser.add_argument("--num_beams", "-b", help="Number of beams for beam search", type=int, default=1)
    parser.add_argument("--do_sample", "-s", help="Use sampling instead of greedy decoding", action="store_true")
    args = parser.parse_args()
    # fmt: on

    data = load_data(task="current_weather", split="dev")
    sample = data[0]

    city_name = sample["name"]
    prompt = f"Write a one-paragraph weather report for {city_name} as of today based on the following data:\n{sample}\n"

    print("Prompt")
    print("=" * 10)
    print(prompt)

    model_args = {
        "max_tokens": args.max_tokens,
        "num_beams": args.num_beams,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "top_k": args.top_k,
        "do_sample": args.do_sample,
        "seed": args.seed,
    }

    # base model
    if args.node == 2:
        output_text = base_model_api(
            node=args.node, model_args=model_args, prompt=prompt
        )
    # instruction-tuned models
    else:
        output_text = instruct_model_api(
            node=args.node, model_args=model_args, prompt=prompt
        )

    print("Model response")
    print("=" * 15)
    print(output_text)
