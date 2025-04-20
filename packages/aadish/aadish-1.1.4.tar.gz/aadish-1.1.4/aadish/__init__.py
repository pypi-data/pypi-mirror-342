# aadish.py
# -*- coding: utf-8 -*-
"""
Aadish: A CLI-based AI assistant using HTTP streaming, ANSI/Rich formatting, and configurable settings.
"""

import os
import sys
import time
import signal
import logging
from typing import Optional, Tuple
import re

import requests
import colorama
from colorama import Fore, Style
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.markup import escape
from rich.text import Text

import pyfiglet

# Initialize Colorama for ANSI support and Rich console
colorama.init(autoreset=True)
console = Console()

# ─── Logging configuration ───────────────────────────────────────────────────
class ColorFormatter(logging.Formatter):
    LEVEL_COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA
    }

    def format(self, record):
        level = record.levelname
        color = self.LEVEL_COLORS.get(level, Fore.WHITE)
        record.levelname = color + level + Style.RESET_ALL
        return super().format(record)

def setup_logging():
    log_level = os.getenv('AADISH_LOG_LEVEL', 'WARNING').upper()
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    fmt = "%(asctime)s %(levelname)s: %(message)s"
    handler = logging.StreamHandler()
    handler.setFormatter(ColorFormatter(fmt))
    root_logger.handlers = [handler]

    # Optional file logging
    log_file = os.getenv('AADISH_LOG_FILE')
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(ColorFormatter(fmt))
        root_logger.addHandler(file_handler)

setup_logging()
logger = logging.getLogger(__name__)

# ─── API and prompts ──────────────────────────────────────────────────────────
API_URL = os.getenv('AADISH_API_URL', 'https://aiaadish.vercel.app/api/chat')
DEFAULT_SYSTEM_PROMPT = (
    "You are Aadish, an AI assistant delivering accurate, reliable information with minimal hallucination. "
    "Verify facts and admit uncertainty when unsure. Format outputs with ANSI and Rich Markdown. Use proper formatting for writing hug paras "
    "Maintain a professional tone"
    "Use emojis sparingly 😊"
)

# ─── Models and commands ──────────────────────────────────────────────────────
AADISH_MODELS = [
    {"name": "llama4", "id": "meta-llama/llama-4-scout-17b-16e-instruct"},
    {"name": "llama3.3", "id": "llama-3.3-70b-versatile"},
    {"name": "mistral", "id": "mistral-saba-24b"},
    {"name": "compound", "id": "compound-beta"},
    {"name": "compoundmini", "id": "compound-beta-mini"},
    {"name": "gemma", "id": "gemma2-9b-it"},
    {"name": "deepseek", "id": "deepseek-r1-distill-llama-70b"},
    {"name": "qwen", "id": "qwen-qwq-32b"},
]
AADISH_COMMANDS = [
    "aadish(message, model='model_id', system=None)",
    "aadishresponse()",
    "aadishtalk(model='model_id', system=None)",
    "aadishcommands()",
    "aadishmodels()"
]

# ─── Configurations ──────────────────────────────────────────────────────────
class AadishConfig:
    def __init__(self):
        self.temperature = float(os.getenv('AADISH_TEMP', 1.0))
        self.top_p = float(os.getenv('AADISH_TOP_P', 1.0))
        self.max_tokens = int(os.getenv('AADISH_MAX_TOKENS', 1024))

config = AadishConfig()
_last_response: Optional[str] = None

# ─── Helper: API interaction ─────────────────────────────────────────────────
def _validate_model(name: str) -> str:
    for m in AADISH_MODELS:
        if name == m['name'] or name == m['id']:
            return m['id']
    valid = ', '.join(m['name'] for m in AADISH_MODELS)
    raise ValueError(f"Invalid model '{name}'. Valid models: {valid}")

def _handle_api_error(resp: requests.Response) -> str:
    try:
        data = resp.json()
        err = data.get('error', data)
        if isinstance(err, dict):
            return err.get('message', 'Unknown API error')
        return str(err)
    except Exception:
        code = resp.status_code
        text = resp.text
        return f"HTTP {code}: {text}"

def _send_request(payload: dict) -> Tuple[Optional[str], Optional[str]]:
    try:
        with requests.post(API_URL, json=payload, headers={'Content-Type': 'application/json'}, stream=True, timeout=60) as r:
            if not r.ok:
                return None, _handle_api_error(r)
            content = ''.join(chunk for chunk in r.iter_content(decode_unicode=True) if chunk)
            return content.strip(), None
    except requests.exceptions.Timeout:
        return None, "Connection timeout. Try again later."
    except requests.exceptions.ConnectionError:
        return None, "Connection error. Check internet and API URL."
    except Exception as e:
        return None, f"Unexpected error: {e}"

# ─── Think-aware Renderer ────────────────────────────────────────────────────
def _render_response(content: str, model_id: str) -> None:
    if any(key in model_id.lower() for key in ['qwen', 'deepseek']):
        think_blocks = re.findall(r'<think>(.*?)</think>', content, re.DOTALL)
        main_text = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
        for tb in think_blocks:
            think_text = Text(tb.strip(), style="grey70 italic dim")
            console.print(Panel(think_text, title="[bold yellow]Model Thinking[/bold yellow]", style="grey23", expand=False))
            console.print("[grey50]" + ("-" * 40) + "[/grey50]")

        if main_text:
            console.print(Markdown(main_text))
    else:
        console.print(Markdown(content))

# ─── User-facing functions ───────────────────────────────────────────────────
def aadish(message: str, model: str = 'compound', system: Optional[str] = None) -> None:
    global _last_response
    if not message.strip():
        console.print(f"{Fore.RED}Error:{Style.RESET_ALL} Message cannot be empty")
        return

    model_id = _validate_model(model)
    payload = {
        'message': message.strip(),
        'model': model_id,
        'system': system or DEFAULT_SYSTEM_PROMPT,
        'temperature': config.temperature,
        'top_p': config.top_p,
        'max_completion_tokens': config.max_tokens
    }
    content, error = _send_request(payload)
    if error:
        console.print(f"{Fore.RED}Error:{Style.RESET_ALL} {error}")
    else:
        _render_response(content, model_id)
        _last_response = content

def aadishresponse() -> Optional[str]:
    return _last_response

def aadishtalk(model: str = 'compound', system: Optional[str] = None) -> None:
    font = os.getenv('AADISH_BANNER_FONT', 'slant')
    banner = pyfiglet.Figlet(font=font).renderText('AADISH')
    model_id = _validate_model(model)
    console.print(f"[bold magenta]{banner}[/bold magenta]")
    console.print(Panel(f"[bold green]Welcome to Aadish interactive chat![/bold green]\n[dim]Model: {model_id}[/dim]\nType your questions below.\nPress Ctrl+C to exit anytime.", title="[bold blue]Aadish Assistant[/bold blue]"))

    history = []

    def _signal_handler(sig, frame):
        console.print(f"\n{Fore.RED}Exiting chat. Goodbye!{Style.RESET_ALL}")
        sys.exit(0)
    signal.signal(signal.SIGINT, _signal_handler)

    while True:
        user_input = console.input(f"[bold blue]You:[/bold blue] ")
        if not user_input.strip():
            continue
        history.append({'role': 'user', 'content': user_input})

        payload = {
            'message': user_input,
            'model': model_id,
            'system': system or DEFAULT_SYSTEM_PROMPT,
            'temperature': config.temperature,
            'top_p': config.top_p,
            'max_completion_tokens': config.max_tokens,
            'history': history[:-1]
        }
        content, error = _send_request(payload)
        if error:
            console.print(f"{Fore.RED}Error:{Style.RESET_ALL} {error}")
        else:
            _render_response(content, model_id)
            history.append({'role': 'assistant', 'content': content})

def aadishcommands() -> None:
    console.print("[bold]Available commands:[/bold]")
    for cmd in AADISH_COMMANDS:
        console.print(f"  • {cmd}")

def aadishmodels() -> None:
    console.print("[bold]Supported AI models:[/bold]")
    for m in AADISH_MODELS:
        console.print(f"• {m['name']} -> {m['id']}")

# ─── CLI entry point ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Aadish: CLI AI assistant',
        epilog='''Examples:
  python aadish.py --talk
  python aadish.py --model gemma "What is the weather today?"
  python aadish.py --model llama3.3 --system "Reply like a poet." "Tell me about love"
''',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--talk', action='store_true', help='Start interactive chat')
    parser.add_argument('--model', default='compound', help='Model name or ID')
    parser.add_argument('--system', help='Override system prompt')
    parser.add_argument('message', nargs=argparse.REMAINDER, help='Message to send')
    args = parser.parse_args()

    if args.talk:
        aadishtalk(model=args.model, system=args.system)
    else:
        msg = ' '.join(args.message).strip()
        if not msg:
            console.print(f"{Fore.RED}Error:{Style.RESET_ALL} No message provided.")
            sys.exit(1)
        aadish(msg, model=args.model, system=args.system)
