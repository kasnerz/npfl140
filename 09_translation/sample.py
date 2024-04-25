#!/usr/bin/env python3

import os
import requests
import argparse
import json
import langcodes

API_KEY = "npfl140"


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

    parser.add_argument("--max_tokens", "-m", help="Maximum number of tokens to generate", type=int, default=300)
    parser.add_argument("--seed", "-r", help="Seed for random number generator", type=int, default=42)
    parser.add_argument("--temperature", "-t", help="Temperature parameter", type=float, default=1.0)
    parser.add_argument("--top_p", "-p", help="Top-p sampling parameter", type=float, default=1.0)
    parser.add_argument("--top_k", "-k", help="Top-k sampling parameter", type=int, default=0)
    parser.add_argument("--num_beams", "-b", help="Number of beams for beam search", type=int, default=1)
    parser.add_argument("--do_sample", "-s", help="Use sampling instead of greedy decoding", action="store_true")
    args = parser.parse_args()

    TRANSLATION_PROMPTS = {
        # mistral
        1: "Translate the following text from {src_lang} into {tgt_lang}:\n{src_sentence}",
        # tower
        2: "Translate the following text from {src_lang} into {tgt_lang}.\n{src_lang}: {src_sentence}.\n{tgt_lang}:",
        # aya
        3: "Translate the following text from {src_lang} into {tgt_lang}:\n{src_sentence}",
        # alma-r
        4: "Translate this from {src_lang} to {tgt_lang}:\n{src_lang}: {src_sentence} \n{tgt_lang}: "
    }

    prompt = TRANSLATION_PROMPTS[args.node].format(src_lang=langcodes.Language(args.src_lang).language_name(),
                                                   tgt_lang=langcodes.Language(args.tgt_lang).language_name(),
                                                   src_sentence=args.src_text)
    print("[prompt]")
    print(prompt)
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

    # ALMA-R is a base model
    if args.node == 4:
        output_text = base_model_api(
            node=args.node, model_args=model_args, prompt=prompt
        )
    # the rest of the models are instruction-tuned
    else:
        output_text = instruct_model_api(
            node=args.node, model_args=model_args, prompt=prompt
        )
    print(output_text)
