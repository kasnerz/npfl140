#!/usr/bin/env python3
import requests
import json


def generate_text(
    prompt,
    model,
    temperature=0.7,
    top_k=50,
    top_p=0.9,
    max_tokens=1000,
):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_k": top_k,
        "top_p": top_p,
        "stream": False,
    }

    response = requests.post(url, json=payload)
    j = json.loads(response.text)

    return j["response"]


if __name__ == "__main__":
    model = "gemma2:2b"

    # Example 1: Generate text
    response = generate_text(
        "Who are you?",
        model=model,
        temperature=0.7,
        top_k=50,
        top_p=0.9,
    )
    print(response)
