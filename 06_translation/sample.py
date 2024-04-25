#!/usr/bin/env python3

import os
import requests
import argparse
import json

API_KEY = "npfl140"


TRANSLATION_PROMPTS = {
    "almar": "Translate this from {src_lang} to {tgt_lang}:\n{src_lang}: {src_sentence} \n{tgt_lang}: ".format,
    "tower": "Translate the following text from {src_lang} into {tgt_lang}.\n"
             "{src_lang}: {src_sentence}.\n"
             "{tgt_lang}:".format,
    "llama": "{src_lang}: {src_sentence} {tgt_lang}: ".format
}

# This is exhaustive list of Tower of ALMA_R tuning languages. This needs to be extended for future.
CODE_TO_LANGUAGE = {'en': 'English', 'de': 'German', 'fr': 'French', 'es': 'Spanish', 'it': 'Italian', 'nl': 'Dutch',
                    'pt': 'Portuguese', 'ru': 'Russian', 'zh': 'Chinese', 'cs': 'Czech', 'is': 'Icelandic'}

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
    parser.add_argument("--src_text", type=str, required=True)
    parser.add_argument("--src_lang", type=str, default="de")
    parser.add_argument("--tgt_lang", type=str, default="en")
    parser.add_argument("--prompt_type", type=str, default="almar")

    parser.add_argument("--max_tokens", "-m", help="Maximum number of tokens to generate", type=int, default=300)
    parser.add_argument("--seed", "-r", help="Seed for random number generator", type=int, default=42)
    parser.add_argument("--temperature", "-t", help="Temperature parameter", type=float, default=1.0)
    parser.add_argument("--top_p", "-p", help="Top-p sampling parameter", type=float, default=1.0)
    parser.add_argument("--top_k", "-k", help="Top-k sampling parameter", type=int, default=0)
    parser.add_argument("--num_beams", "-b", help="Number of beams for beam search", type=int, default=1)
    parser.add_argument("--do_sample", "-s", help="Use sampling instead of greedy decoding", action="store_true")
    args = parser.parse_args()

    if args.prompt_type not in TRANSLATION_PROMPTS:
        raise ValueError(f"Unknown prompt type: {args.prompt_type}")
    if args.src_lang not in CODE_TO_LANGUAGE:
        raise ValueError(f"Unknown source language code: {args.src_lang}. Extending list could be enough. Check if the language is supported.")
    if args.tgt_lang not in CODE_TO_LANGUAGE:
        raise ValueError(f"Unknown target language code: {args.tgt_lang}. Extending list could be enough. Check if the language is supported.")

    prompt = TRANSLATION_PROMPTS[args.prompt_type](src_lang=CODE_TO_LANGUAGE[args.src_lang],
                                                   tgt_lang=CODE_TO_LANGUAGE[args.tgt_lang],
                                                   src_sentence=args.src_text)

    print("[prompt]")
    print(prompt)

    print(f"[info]")
    print(f"Words: {len(prompt.split())}, Characters: {len(prompt)}")

    """
	 If you want to count the approximate number of tokens in the output text, you need to first install the transformers library: `pip install transformers`. Then you can use the following code
	"""

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