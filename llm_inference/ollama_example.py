#!/usr/bin/env python3
import json

import requests


def generate_text(
    prompt,
    model,
    temperature=0.7,
    top_k=50,
    top_p=0.9,
    max_tokens=1000,
):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
            "top_k": top_k,
            "top_p": top_p,
        },
        "stream": False,
    }

    response = requests.post(url, json=payload)
    j = json.loads(response.text)

    return j["message"]["content"]


if __name__ == "__main__":
    model = "llama3.2:1b"

    # Example 1: Generate text
    response = generate_text(
        "Who are you?",
        model=model,
        temperature=5.0,
        top_k=500000,
        top_p=1.0,
        max_tokens=400,
    )
    print(response)
