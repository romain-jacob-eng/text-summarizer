# Project 9 — Text Summarizer
# Reads a text file and generates structured summaries at multiple
# levels of detail using the Anthropic API.

import os
from pathlib import Path
from dotenv import load_dotenv
import anthropic


def load_client():
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)
    return client


def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()


def summarize(client, text, mode):
    if mode == "short":
        prompt = f"Summarize the following text in one sentence: {text}"
    elif mode == "paragraph":
        prompt = f"Summarize the following text in a concise paragraph: {text}"
    elif mode == "bullets":
        prompt = f"Summarize the following text in 5 bullet points: {text}"
    else:
        raise ValueError("Invalid mode. Choose 'short', 'paragraph', or 'bullets'.")

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def display_summary(mode, summary):
    print(f"\n--- {mode.capitalize()} Summary ---")
    print(summary)


if __name__ == "__main__":
    client = load_client()
    filepath = Path("input.txt")
    text = read_file(filepath)

    for mode in ["short", "paragraph", "bullets"]:
        summary = summarize(client, text, mode)
        display_summary(mode, summary)