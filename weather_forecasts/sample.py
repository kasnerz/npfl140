#!/usr/bin/env python3

import os
import requests
import argparse
import json

# DO NOT MODIFY THIS MAPPING!
node_to_model_mapping = {
    "1": "llama3.1:8b",
    "2": "phi3.5:3.8b",
    "3": "deepseek-r1:14b",
    "4": "mistral:7b-text",
}


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


def model_api(node, model_args, prompt, system_msg=None, stream=False):
    API_URL = (
        f"http://quest.ms.mff.cuni.cz/nlg/text-generation-api-node{node}/api/generate"
    )

    # Format the request for Ollama API
    ollama_data = {
        "model": node_to_model_mapping[str(node)],  # do not modify
        "prompt": prompt,
        "options": model_args,
        "system": system_msg,
        "stream": stream,
    }

    # Send the request
    response = requests.post(API_URL, json=ollama_data, stream=True)
    response.raise_for_status()

    return response


if __name__ == "__main__":
    # fmt: off
    parser = argparse.ArgumentParser()
    parser.add_argument("--node", "-n", help="Node number (see the instructions for details)", type=int, required=True) 
    parser.add_argument("--task", help="Which data to use", type=str, choices=["current_weather", "forecast"], default="current_weather")
    parser.add_argument("--max_tokens", "-m", help="Maximum number of tokens to generate", type=int, default=500) 
    parser.add_argument("--seed", "-r", help="Seed for random number generator", type=int, default=42) 
    parser.add_argument("--temperature", "-t", help="Temperature parameter", type=float, default=1.0) 
    parser.add_argument("--top_p", "-p", help="Top-p sampling parameter", type=float, default=1.0) 
    parser.add_argument("--top_k", "-k", help="Top-k sampling parameter", type=int, default=0)
    parser.add_argument("--repeat_penalty", help="Repeat penalty parameter", type=float, default=1.0)
    parser.add_argument("--stream", help="Generate a stream of tokens instead of a single response", action="store_true")
    parser.add_argument("--forecast_pruning_factor", help="Keep every n-th item for the forecasts. The original resolution is every 3 hours, using the factor of 2 keeps the forecast for every 6 hours.", type=int, default=1)
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

        print("=" * 80)
        print("[PROMPT]", prompt)

        print(f"[INFO] Words: {len(prompt.split())}, Characters: {len(prompt)}")

        # see https://github.com/ollama/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values
        model_args = {
            "num_predict": args.max_tokens,
            "temperature": args.temperature,
            "top_p": args.top_p,
            "top_k": args.top_k,
            "seed": args.seed,
            "repeat_penalty": args.repeat_penalty,
        }

        response = model_api(
            node=args.node,
            model_args=model_args,
            prompt=prompt,
            stream=args.stream,
            system_msg=None,  # Set to a string if you want to provide additional information to the model
        )

        if args.stream:
            print("[OUTPUT]", end=" ", flush=True)
            for line in response.iter_lines():
                if line:
                    chunk_data = json.loads(line.decode("utf-8"))
                    chunk_text = chunk_data.get("response", "")
                    print(chunk_text, end="", flush=True)
            print()  # Add a newline at the end
        else:
            text = response.json()["response"]

            print("[OUTPUT]", text)

        # remove to generate output for all samples
        break
