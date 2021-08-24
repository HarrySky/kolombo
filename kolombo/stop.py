from typer import Context, Typer

from kolombo.configuration_files import generate_senders_compose_config
from kolombo.console import debug, error, step
from kolombo.util import (
    async_command,
    execute_as_root,
    needs_database,
    run,
    stop_kolombo_service,
)

stop_cli = Typer(invoke_without_command=True)


@stop_cli.callback()
def stop_main(ctx: Context) -> None:
    if ctx.invoked_subcommand is None:
        debug("Stopping all Kolombo services")
        # TODO


@stop_cli.command("receiver")
@execute_as_root
def stop_receiver() -> None:
    step("Stopping receiver service")
    stop_kolombo_service("receiver")


@stop_cli.command("auth")
@execute_as_root
def stop_auth() -> None:
    step("Stopping auth service")
    stop_kolombo_service("auth")


@stop_cli.command("nginx")
@execute_as_root
def stop_nginx() -> None:
    step("Stopping nginx service")
    stop_kolombo_service("nginx")


@stop_cli.command("senders")
@execute_as_root
@async_command
@needs_database
async def stop_senders() -> None:
    from kolombo.models import Domain

    domains = {domain.actual for domain in await Domain.all_active()}
    if len(domains) < 1:
        error("No active domains to stop senders for")
        exit(1)

    senders_compose_config = generate_senders_compose_config(domains)
    project_name = "kolombo_senders"
    file_path = "/etc/kolombo/senders-compose.yml"
    with open(file_path, mode="w") as compose_file:
        compose_file.write(senders_compose_config)

    compose_command = ["docker-compose", "-p", project_name, "-f", file_path, "down"]
    run([*compose_command, "--remove-orphans"])
