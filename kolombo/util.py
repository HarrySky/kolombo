import sys
from asyncio import run as run_async
from functools import wraps

if sys.version_info >= (3, 9):
    from importlib.resources import files
else:
    from importlib_resources import files

from os import execvp, getuid
from os.path import realpath

# Security implications are considered
from subprocess import STDOUT, check_output  # nosec: B404
from typing import Any, Awaitable, Callable, List

from docker import DockerClient  # type: ignore[import]

from kolombo.console import step, warning


def run(command: List[str], as_root: bool = False) -> str:
    if as_root and getuid() != 0:
        command.insert(0, "sudo")

    # We trust input here, it does not come from user
    return check_output(command, text=True, stderr=STDOUT)  # nosec: B603


def async_command(func: Callable[..., Awaitable[None]]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        run_async(func(*args, **kwargs))

    return wrapper


def needs_database(
    func: Callable[..., Awaitable[None]]
) -> Callable[..., Awaitable[Any]]:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        from kolombo.models import init_database

        await init_database()
        await func(*args, **kwargs)

    return wrapper


def execute_as_root(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if getuid() == 0:
            func(*args, **kwargs)
            return

        warning("Executing as root via sudo!")
        script_path = realpath(sys.argv[0])
        arguments = sys.argv[1:]
        execvp("sudo", ["sudo", script_path, *arguments])  # nosec: B606, B607

    return wrapper


def build_kolombo_image(client: DockerClient, service: str) -> None:
    kolombo_folder = files("kolombo")
    step(f"Building [code]kolombo-{service}[/] image")
    client.images.build(
        tag=f"kolombo-{service}",
        path=str(kolombo_folder),
        pull=True,
        nocache=True,
        rm=True,
        dockerfile=f"docker/Dockerfile.{service}",
    )


def up_all_kolombo_services() -> None:
    project_name = "kolombo_services"
    docker_folder = files("kolombo") / "docker"
    file_path = str(docker_folder / "services" / "docker-compose.yml")
    compose_command = ["docker-compose", "-p", project_name, "-f", file_path, "up"]
    run([*compose_command, "--force-recreate", "-d"])


def up_kolombo_service(service: str) -> None:
    project_name = "kolombo_services"
    docker_folder = files("kolombo") / "docker"
    file_path = str(docker_folder / "services" / "docker-compose.yml")
    compose_command = ["docker-compose", "-p", project_name, "-f", file_path, "up"]
    run([*compose_command, "--no-deps", "--force-recreate", "-d", f"kolombo-{service}"])


def stop_all_kolombo_services() -> None:
    project_name = "kolombo_services"
    docker_folder = files("kolombo") / "docker"
    file_path = str(docker_folder / "services" / "docker-compose.yml")
    run(["docker-compose", "-p", project_name, "-f", file_path, "down"])


def stop_kolombo_service(service: str) -> None:
    project_name = "kolombo_services"
    docker_folder = files("kolombo") / "docker"
    file_path = str(docker_folder / "services" / "docker-compose.yml")
    compose_command = ["docker-compose", "-p", project_name, "-f", file_path, "rm"]
    run([*compose_command, "--stop", "--force", f"kolombo-{service}"])
