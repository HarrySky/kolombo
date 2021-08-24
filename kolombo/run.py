from docker import from_env  # type: ignore[import]
from typer import Context, Typer

from kolombo.configuration_files import generate_senders_compose_config
from kolombo.console import debug, error, step
from kolombo.util import (
    async_command,
    build_kolombo_image,
    execute_as_root,
    needs_database,
    run,
    up_kolombo_service,
)

run_cli = Typer(invoke_without_command=True)


@run_cli.callback()
def run_main(ctx: Context) -> None:
    if ctx.invoked_subcommand is None:
        debug("Deploying all Kolombo services")
        # TODO


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

    compose_command = ["docker-compose", "-p", project_name, "-f", file_path, "up"]
    run([*compose_command, "--force-recreate", "--remove-orphans", "-d"])
