"""
Memory management for GPT-CLI.

Includes functions to load, save, reset, and summarize conversational memory.
"""

import json
import os

from openai import OpenAI, OpenAIError
from rich.console import Console

console = Console()


def load_memory(memory_path: str) -> tuple[str, list]:
    """
    Load memory from the given path. Returns (rolling_summary, recent_messages).
    """
    if os.path.exists(memory_path):
        try:
            with open(memory_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("summary", ""), data.get("recent", [])
        except json.JSONDecodeError:
            console.print("[bold red]⚠️ Corrupted memory file. Resetting...[/bold red]")
            return "", []
    return "", []


def save_memory(memory_path: str, rolling_summary: str, recent_messages: list):
    """
    Save memory to the given path.
    """
    with open(memory_path, "w", encoding="utf-8") as f:
        json.dump({"summary": rolling_summary, "recent": recent_messages}, f, indent=2)
    os.chmod(memory_path, 0o600)


def reset_memory(memory_path: str) -> tuple[str, list]:
    """
    Delete memory file if it exists, and return an empty summary and message list.
    """
    if os.path.exists(memory_path):
        try:
            os.remove(memory_path)
            console.print("[bold yellow]🧹 Memory file has been reset.[/bold yellow]\n")
        except PermissionError:
            console.print(
                "[bold red]⚠️ Failed to reset memory file due to permission error.[/bold red]"
            )
            return "", []
    else:
        console.print("[blue]ℹ️ No memory file to reset.[/blue]\n")
    return "", []


def summarize_recent(
    client: OpenAI,
    model: str,
    memory_path: str,
    rolling_summary: str,
    recent_messages: list,
    memory_limit: int,
    max_summary_tokens: int,
) -> tuple[str, list]:
    """
    Generate a new summary from the recent messages and clear the recent_messages.
    Returns updated (rolling_summary, recent_messages).
    """
    if not recent_messages:
        save_memory(memory_path, rolling_summary, [])
        return rolling_summary, []

    batch = recent_messages[-(memory_limit * 2) :]
    summary_prompt = (
        f"Here is the current summary of our conversation:\n{rolling_summary}\n\n"
        f"Please update it with the following messages:\n"
        + "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in batch])
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a summarizer that maintains a concise "
                    "summary of a conversation.",
                },
                {"role": "user", "content": summary_prompt},
            ],
            temperature=0,
            max_tokens=max_summary_tokens,
        )
        new_summary = response.choices[0].message.content.strip()
        save_memory(memory_path, new_summary, [])
        return new_summary, []
    except (OpenAIError, Exception) as e:
        console.print(f"[bold red]Summary failed:[/bold red] {e}")
        return rolling_summary, recent_messages
