from asyncio import run
from functools import wraps
from importlib.resources import path as resource_path

# Security implications are considered
from subprocess import STDOUT, CalledProcessError, check_output  # nosec: B404
from typing import Any, Awaitable, Callable, List, Optional, Union

from rich.console import Console
from rich.markdown import Markdown


def async_command(func: Callable[..., Awaitable[None]]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return run(func(*args, **kwargs))

    return wrapper


def run_command(command: str, sudo: bool = False) -> str:
    cmd = command.split(" ")
    if sudo:
        cmd.insert(0, "sudo")
    # We trust input here, it does not come from user
    return check_output(cmd, text=True, stderr=STDOUT)  # nosec: B603


def docker(command: str) -> str:
    return run_command(f"docker {command}", sudo=True)


def kolombo_image_exists(component: str) -> bool:
    try:
        docker(f"image inspect kolombo-{component}")
        return True
    except CalledProcessError:
        return False


def build_kolombo_image(component: str) -> str:
    with resource_path(package="kolombo", resource=".") as context:
        dockerfile = f"{context}/docker/{component}/Dockerfile"
        return docker(
            f"build --no-cache -f {dockerfile} -t kolombo-{component} {context}"
        )


def run_container(
    image: str,
    args: Optional[str] = None,
    *,
    name: Optional[str] = None,
    net: Optional[str] = None,
    volumes: Optional[List[str]] = None,
    ports: Optional[List[str]] = None,
    other_flags: str = "-d",
) -> str:
    cmd = "run"
    if args is not None:
        image += f" {args}"
    if name is not None:
        cmd += f" --name {name}"
    if net is not None:
        cmd += f" --net {net}"
    if volumes:
        cmd += f" -v {' -v '.join(volumes)}"
    if ports:
        cmd += f" -p {' -p '.join(ports)}"

    return docker(f"{cmd} {other_flags} {image}")


def create_network(network: str, subnet: str) -> str:
    # Create only if does not exist
    if not docker(f"network ls -q --filter name={network}"):
        return docker(f"network create {network} --subnet={subnet}")
    return "Network already created"


class CliLog:
    def __init__(self) -> None:
        self._console = Console()

    def step(self, message: Union[str, Markdown]) -> None:
        self._console.print(message, style="bold green")

    def info(self, message: Union[str, Markdown]) -> None:
        self._console.print(message, style="bold cyan")

    def error(self, message: Union[str, Markdown]) -> None:
        self._console.print(message, style="bold red")
