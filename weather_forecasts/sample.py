#!/usr/bin/env python3

import argparse
import json
import os

import requests


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


def model_api(node, model_args, prompt, api_key, is_chat=True):
    base_url = f"https://quest.ms.mff.cuni.cz/nlg/text-generation-api-node{node}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    if is_chat:
        url = f"{base_url}/v1/chat/completions"
        payload = {
            "model": "default",
            "messages": [{"role": "user", "content": prompt}],
            **model_args,
        }
    else:
        url = f"{base_url}/v1/completions"
        payload = {"model": "default", "prompt": prompt, **model_args}

    # Send the request
    response = requests.post(url, json=payload, headers=headers, timeout=120)
    response.raise_for_status()

    return response, is_chat


def is_base_model(node_number):
    return node_number == 4


if __name__ == "__main__":
    # fmt: off
    parser = argparse.ArgumentParser()
    parser.add_argument("--node", "-n", help="Node number (1-4)", type=int, required=True) 
    parser.add_argument("--api-key", help="API Key for the vLLM server", type=str, default="AiTxk0ar6gz3ysD")
    parser.add_argument("--task", help="Which data to use", type=str, choices=["current_weather", "forecast"], default="current_weather")
    parser.add_argument("--max-tokens", "-m", help="Maximum number of tokens to generate", type=int, default=10000) 
    parser.add_argument("--temperature", "-t", help="Temperature parameter", type=float, default=1.0) 
    parser.add_argument("--top-p", "-p", help="Top-p sampling parameter", type=float, default=1.0) 
    parser.add_argument("--top-k", "-k", help="Top-k sampling parameter", type=int, default=50)
    parser.add_argument("--forecast-pruning-factor", help="Keep every n-th item for the forecasts. The original resolution is every 3 hours, using the factor of 2 keeps the forecast for every 6 hours.", type=int, default=1)
    args = parser.parse_args()
    # fmt: on

    data = load_data(
        task=args.task, forecast_pruning_factor=args.forecast_pruning_factor
    )

    for sample in data:
        city_name = (
            sample["name"] if args.task == "current_weather" else sample["city"]["name"]
        )
        if args.task == "forecast":
            prompt = f"Write a one-paragraph 5-day weather forecast for {city_name} based on the following data:\n{sample}\n"
        elif args.task == "current_weather":
            prompt = f"Write a one-paragraph weather report for {city_name} as of today based on the following data:\n{sample}\n"

        print("=" * 80)
        print("[PROMPT]", prompt)

        print(f"[INPUT] Words: {len(prompt.split())}, Characters: {len(prompt)}")

        # see vLLM API parameters
        model_args = {
            "max_tokens": args.max_tokens,
            "temperature": args.temperature,
            "top_p": args.top_p,
            "top_k": args.top_k,
        }

        response, is_chat = model_api(
            node=args.node,
            model_args=model_args,
            prompt=prompt,
            api_key=args.api_key,
            is_chat=not is_base_model(args.node),
        )

        data = response.json()
        if is_chat:
            message = data["choices"][0]["message"]
            reasoning = message.get("reasoning_content") or message.get("reasoning")
            if reasoning:
                print("\n--- Thinking... ---")
                print(reasoning)
                print("------------------------")
            print("[OUTPUT]\n", message.get("content"))
        else:
            print("[OUTPUT]\n", data["choices"][0]["text"])

        # remove to generate output for all samples
        break
