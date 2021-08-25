from docker import from_env  # type: ignore[import]
from typer import Typer

from kolombo.configuration_files import generate_senders_compose_config
from kolombo.console import error, step
from kolombo.util import (
    async_command,
    build_kolombo_image,
    execute_as_root,
    needs_database,
    run,
    up_all_kolombo_services,
    up_kolombo_service,
)

run_cli = Typer()


@run_cli.command("all")
@execute_as_root
@async_command
@needs_database
async def run_all() -> None:
    from kolombo.models import Domain

    client = from_env()
    build_kolombo_image(client, "receiver")
    build_kolombo_image(client, "auth")
    build_kolombo_image(client, "nginx")
    build_kolombo_image(client, "sender")

    step("Deploying all Kolombo services")
    up_all_kolombo_services()

    domains = [domain.actual for domain in await Domain.all_active()]
    # Remove duplicates preserving order
    domains = list(dict.fromkeys(domains))
    if len(domains) < 1:
        error("No active domains to run senders for")
        return

    senders_compose_config = generate_senders_compose_config(domains)
    project_name = "kolombo_senders"
    file_path = "/etc/kolombo/senders-compose.yml"
    with open(file_path, mode="w") as compose_file:
        compose_file.write(senders_compose_config)

    step(f"Deploying senders for domains: {', '.join(domains)}")
    compose_command = ["docker-compose", "-p", project_name, "-f", file_path, "up"]
    run([*compose_command, "--force-recreate", "--remove-orphans", "-d"])


@run_cli.command("receiver")
@execute_as_root
def run_receiver() -> None:
    client = from_env()
    build_kolombo_image(client, "receiver")

    step("Bringing up receiver service")
    up_kolombo_service("receiver")


@run_cli.command("auth")
@execute_as_root
def run_auth() -> None:
    client = from_env()
    build_kolombo_image(client, "auth")

    step("Bringing up auth service")
    up_kolombo_service("auth")


@run_cli.command("nginx")
@execute_as_root
def run_nginx() -> None:
    client = from_env()
    build_kolombo_image(client, "nginx")

    step("Bringing up nginx service")
    up_kolombo_service("nginx")


@run_cli.command("senders")
@execute_as_root
@async_command
@needs_database
async def run_senders() -> None:
    from kolombo.models import Domain

    domains = [domain.actual for domain in await Domain.all_active()]
    # Remove duplicates preserving order
    domains = list(dict.fromkeys(domains))
    if len(domains) < 1:
        error("No active domains to run senders for")
        exit(1)

    client = from_env()
    build_kolombo_image(client, "sender")

    senders_compose_config = generate_senders_compose_config(domains)
    project_name = "kolombo_senders"
    file_path = "/etc/kolombo/senders-compose.yml"
    with open(file_path, mode="w") as compose_file:
        compose_file.write(senders_compose_config)

    step(f"Deploying senders for domains: {', '.join(domains)}")
    compose_command = ["docker-compose", "-p", project_name, "-f", file_path, "up"]
    run([*compose_command, "--force-recreate", "--remove-orphans", "-d"])
