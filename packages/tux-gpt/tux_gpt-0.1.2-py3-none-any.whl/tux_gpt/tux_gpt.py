#!/usr/bin/env python3
import os
import sys
import json
import atexit
import platform
from pathlib import Path
from typing import Any, Dict, List
try:
    import readline
except ImportError:
    readline = None
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

 
def get_config_dir() -> Path:
    """Return the configuration directory for tux-gpt based on OS."""
    if os.name == "nt":
        base = Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "tux-gpt"

CONFIG_DIR: Path = get_config_dir()
CONFIG_PATH: Path = CONFIG_DIR / "config.json"
HISTORY_PATH: Path = CONFIG_DIR / "history.json"
INPUT_HISTORY_PATH: Path = CONFIG_DIR / "input_history"
MAX_HISTORY: int = 20



def write_default_config() -> None:
    """Create default configuration file with default model."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    default_config: Dict[str, str] = {"model": "gpt-4.1-mini"}
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(default_config, f, indent=2)


def load_config() -> Dict[str, Any]:
    """Load CLI configuration, writing default if missing."""
    if not CONFIG_PATH.exists():
        write_default_config()
    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: failed to load config {CONFIG_PATH}: {e}")
        return {"model": "gpt-4.1-mini"}
    
def load_history() -> List[Dict[str, str]]:
    """Load persisted conversation history (up to MAX_HISTORY)."""
    if not HISTORY_PATH.exists():
        return []
    try:
        with HISTORY_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: failed to load history {HISTORY_PATH}: {e}")
        return []

def save_history(history: List[Dict[str, str]]) -> None:
    """Persist conversation history, keeping only last MAX_HISTORY messages."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with HISTORY_PATH.open("w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Warning: failed to save history {HISTORY_PATH}: {e}")


def main() -> None:
    """Main entry point for tux-gpt CLI."""
    console = Console()
    # ensure config directory exists
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    # setup input line history if available
    if readline:
        try:
            readline.read_history_file(str(INPUT_HISTORY_PATH))
        except Exception:
            pass
        atexit.register(lambda: readline.write_history_file(str(INPUT_HISTORY_PATH)))

    welcome_message = """\

                     Welcome to the tux-gpt!
          This is a terminal-based interactive tool using GPT.
         Please, visit us at https://github.com/fberbert/tux-gpt
                      Type 'exit' to quit.
    """

    console.print(f"[bold blue]{welcome_message}[/bold blue]", justify="left")

    api_key: str = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        console.print("[red]Please set your OPENAI_API_KEY environment variable.[/red]")
        sys.exit(1)

    config: Dict[str, Any] = load_config()
    model: str = config.get("model", "gpt-4.1-mini")
    # check model compatibility
    supported_models = ("gpt-4.1", "gpt-4.1-mini")
    if model not in supported_models:
        console.print(f"[red]Model '{model}' not supported. Choose one of: {', '.join(supported_models)}[/red]")
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    console = Console()

    # System prompt: allow Markdown output
    system_msg = {
        "role": "system",
        "content": (
            "You are a virtual assistant that can search the web. "
            "Always search the web when user asks for something data related. "
            "For example: 'What is the weather today?' or 'Which date is today?'. "
            "You are running in a Linux terminal. "
            "Return responses formatted in Markdown so they can be rendered in the terminal using rich."
        )
    }
    # load persisted conversation (last MAX_HISTORY messages)
    persisted = load_history()

    # main REPL loop
    while True:
        try:
            user_input = input("> ")
        except (EOFError, KeyboardInterrupt):
            console.print("\nExiting.")
            break
        # ignore empty input
        if not user_input.strip():
            continue
        # handle exit commands without sending to model
        if user_input.strip().lower() in ("exit", "quit"):
            console.print("Exiting.")
            break
        # build messages for API: system + last persisted + current user
        call_history = [system_msg] + persisted + [{"role": "user", "content": user_input}]
        # call API with rich spinner/status
        try:
            with console.status("[bold green]", spinner="dots"):
                resp = client.responses.create(
                    model=model,
                    input=call_history,
                    tools=[{"type": "web_search_preview"}]
                )
        except Exception as e:
            console.print(f"[red]Error calling OpenAI API: {e}[/red]")
            continue
        # render and persist response
        answer = resp.output_text.strip()
        console.print()
        console.print(Markdown(answer))
        console.print()
        # update persisted history and save
        persisted.append({"role": "user", "content": user_input})
        persisted.append({"role": "assistant", "content": answer})
        # keep only last MAX_HISTORY messages
        if len(persisted) > MAX_HISTORY:
            persisted = persisted[-MAX_HISTORY:]
        save_history(persisted)


if __name__ == "__main__":
    main()

