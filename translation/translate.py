#!/usr/bin/env python3

import argparse

import requests


API_KEY = "PUtoW1ynfiZqv7C9"

# This is exhaustive list of Tower of ALMA_R tuning languages. This needs to be extended for future.
CODE_TO_LANGUAGE = {'en': 'English', 'de': 'German', 'fr': 'French', 'es': 'Spanish', 'it': 'Italian', 'nl': 'Dutch',
                    'pt': 'Portuguese', 'ru': 'Russian', 'zh': 'Chinese', 'cs': 'Czech', 'is': 'Icelandic'}


def model_api(node, model_args, prompt):
    base_url = f"https://quest.ms.mff.cuni.cz/nlg/text-generation-api-node{node}"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    url = f"{base_url}/v1/chat/completions"
    payload = {
        "model": "default",
        "messages": [{"role": "user", "content": prompt}],
        **model_args,
    }

    response = requests.post(url, json=payload, headers=headers, timeout=120)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    # fmt: off
    parser = argparse.ArgumentParser()
    parser.add_argument("--node", "-n", help="Node number (1-4)", type=int, required=True)
    parser.add_argument("--src_text", type=str, required=True)
    parser.add_argument("--src_lang", type=str, default="de")
    parser.add_argument("--tgt_lang", type=str, default="en")

    parser.add_argument("--max_tokens", "-m", help="Maximum number of tokens to generate", type=int, default=300)
    parser.add_argument("--temperature", "-t", help="Temperature parameter", type=float, default=1.0)
    parser.add_argument("--top_p", "-p", help="Top-p sampling parameter", type=float, default=1.0)
    parser.add_argument("--top_k", "-k", help="Top-k sampling parameter", type=int, default=50)
    args = parser.parse_args()
    # fmt: on

    if args.src_lang not in CODE_TO_LANGUAGE:
        raise ValueError(f"Unknown source language code: {args.src_lang}. Extending list could be enough. Check if the language is supported.")
    if args.tgt_lang not in CODE_TO_LANGUAGE:
        raise ValueError(f"Unknown target language code: {args.tgt_lang}. Extending list could be enough. Check if the language is supported.")

    src_lang = CODE_TO_LANGUAGE[args.src_lang]
    tgt_lang = CODE_TO_LANGUAGE[args.tgt_lang]
    prompt = f"{src_lang}: {args.src_text} {tgt_lang}: "

    print("[prompt]")
    print(prompt)

    print(f"[info]")
    print(f"Words: {len(prompt.split())}, Characters: {len(prompt)}")

    print()
    print("[output]")

    model_args = {
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "top_k": args.top_k,
    }

    output_text = model_api(node=args.node, model_args=model_args, prompt=prompt)
    print(output_text)

    # remove to generate output for all samples