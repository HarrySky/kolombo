from typing import Any, List

from rich.console import Console
from rich.markdown import Markdown

_console = Console()
_debug_mode = False


def started(message: str) -> None:
    """Message to indicate that command is started"""
    _console.print(message, style="underline")
    _console.line()


def step(message: str) -> None:
    """Message to indicate current step"""
    _console.print(f"> {message}", style="bold green")


def finished(message: str) -> None:
    """Message to indicate that command is finished"""
    _console.line()
    _console.print(f":checkered_flag: {message}", style="green")


def info(message: str) -> None:
    _console.print(message)


def print_list(list_to_print: List[Any]) -> None:
    _console.print(Markdown(f"*  {'* '.join(list_to_print)}"))


def warning(message: str) -> None:
    _console.print(f":warning-text: {message}", style="underline bold orange1")


def error(message: str) -> None:
    _console.print(f":x-text: {message}", style="bold red")


def enable_debug() -> None:
    global _debug_mode
    _debug_mode = True


def debug(message: str) -> None:
    if _debug_mode:
        _console.print(f"[DEBUG] {message}", style="italic cyan")
