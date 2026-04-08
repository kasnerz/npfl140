#!/usr/bin/env python3

import argparse

from langcodes import Language, tag_is_valid
import requests
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint

console = Console()

# TODO: Fill the API key according to the instructions.
API_KEY = "npfl140" 

if not API_KEY:
    raise ValueError("API key is not set. Please fill the API_KEY according to the instructions.")

def language_name_from_code(code):
    normalized_code = code.strip().lower()
    if not tag_is_valid(normalized_code):
        raise ValueError(f"Unknown language code: {code}. Check if the language is supported.")

    language_name = Language.get(normalized_code).display_name("en")
    if not language_name or language_name.lower() == normalized_code:
        raise ValueError(f"Unknown language code: {code}. Check if the language is supported.")

    return language_name


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

    src_lang = language_name_from_code(args.src_lang)
    tgt_lang = language_name_from_code(args.tgt_lang)
    prompt = f"Translate the following from {src_lang} to {tgt_lang}:\n\n{args.src_text}"

    console.print(Panel(prompt, title="[bold cyan]Prompt[/bold cyan]", border_style="cyan"))
    console.print(f"[bold yellow]Words:[/bold yellow] {len(prompt.split())}  [bold yellow]Characters:[/bold yellow] {len(prompt)}")
    console.print()

    model_args = {
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "top_k": args.top_k,
    }

    output_text = model_api(node=args.node, model_args=model_args, prompt=prompt)
    console.print(Panel(output_text, title="[bold green]Output[/bold green]", border_style="green"))

    # remove to generate output for all samples