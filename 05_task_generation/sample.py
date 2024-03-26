#!/usr/bin/env python3

import os
import requests
import argparse
import json

API_KEY = "npfl140"


def load_data(task, forecast_pruning_factor):
    data = []
    dir_path = os.path.join("data", task)

    for filename in sorted(os.listdir(dir_path)):
        file_path = os.path.join(dir_path, filename)

        with open(file_path) as f:
            data.append(json.load(f))

    if task == "forecast" and forecast_pruning_factor > 1:
        for item in data:
            item["list"] = item["list"][::forecast_pruning_factor]

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
    try:
        output_text = response.json()["choices"][0]["text"]
        return output_text
    except:
        print(f"API error message: {response}")


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
    try:
        output_text = response.json()["choices"][0]["message"]["content"]
        return output_text
    except:
        print(f"API error message: {response}")


if __name__ == "__main__":
    # fmt: off
    parser = argparse.ArgumentParser()
    parser.add_argument("--node", "-n", help="Node number (see the instructions for details)", type=int, required=True) 
    parser.add_argument("--task", help="Which data to use", type=str, choices=["current_weather", "forecast"], default="current_weather")
    parser.add_argument("--max_tokens", "-m", help="Maximum number of tokens to generate", type=int, default=300) 
    parser.add_argument("--seed", "-r", help="Seed for random number generator", type=int, default=42) 
    parser.add_argument("--temperature", "-t", help="Temperature parameter", type=float, default=1.0) 
    parser.add_argument("--top_p", "-p", help="Top-p sampling parameter", type=float, default=1.0) 
    parser.add_argument("--top_k", "-k", help="Top-k sampling parameter", type=int, default=0)
    parser.add_argument("--num_beams", "-b", help="Number of beams for beam search", type=int, default=1)
    parser.add_argument("--forecast_pruning_factor", help="Keep every n-th item for the forecasts. The original resolution is every 3 hours, using the factor of 2 keeps the forecast for every 6 hours.", type=int, default=1)
    parser.add_argument("--do_sample", "-s", help="Use sampling instead of greedy decoding", action="store_true")
    args = parser.parse_args()
    # fmt: on

    data = load_data(
        task=args.task, forecast_pruning_factor=args.forecast_pruning_factor
    )

    for sample in data:
        city_name = (
            sample["name"] if args.task == "current_weather" else sample["city"]["name"]
        )
        prompt = f"Write a one-paragraph weather report for {city_name} as of today based on the following data:\n{sample}\n"

        print("[prompt]")
        print(prompt)

        print(f"[info]")
        print(f"Words: {len(prompt.split())}, Characters: {len(prompt)}")

        """
         If you want to count the approximate number of tokens in the output text, you need to first install the transformers library: `pip install transformers`. Then you can use the following code
        """
        # from transformers import AutoTokenizer

        # tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
        # tokens = tokenizer(prompt)
        # print(f"Tokens: {len(tokens['input_ids'])}")

        print()
        print("[output]")

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

        print(output_text)

        # remove to generate output for all samples
        break
