from typer import Option, Typer

from kolombo.bin.util import (
    CliLog,
    async_command,
    build_kolombo_image,
    create_network,
    kolombo_image_exists,
    run_container,
)
from kolombo.models import Domain

cli = Typer()
_component_volumes = {
    "auth": ["/etc/kolombo:/etc/kolombo"],
    "nginx": [
        "/etc/kolombo/mail-enabled:/etc/nginx/mail-enabled",
        "/etc/letsencrypt:/etc/letsencrypt:ro",
    ],
    "receiver": [
        "/etc/kolombo/maildirs:/var/mail",
        "/etc/kolombo/virtual:/etc/postfix/virtual",
    ],
}


def run_kolombo_component(component: str, build: bool) -> None:
    log = CliLog()
    if build or not kolombo_image_exists(component):
        log.step(f"- Building kolombo-{component}")
        build_kolombo_image(component=component)

    log.step("- Creating kolombo network (if does not exist)")
    create_network("kolombo", subnet="192.168.79.0/24")

    log.step(f"- Running kolombo-{component} container")
    ports = None
    if component == "receiver":
        ports = ["25:25"]
    elif component == "nginx":
        ports = ["587:587", "993:993"]

    # Attach TTY (for receiver) and run in background
    other_flags = "-t -d" if component == "receiver" else "-d"
    run_container(
        f"kolombo-{component}",
        name=f"kolombo-{component}",
        net="kolombo",
        volumes=_component_volumes[component],
        ports=ports,
        other_flags=other_flags,
    )


@cli.command("receiver")
def run_receiver(
    conf: str = Option(None, help="Path to .env file with configuration"),  # noqa: B008
    build: bool = Option(False, help="Whether to skip build step"),  # noqa: B008
) -> None:
    run_kolombo_component("receiver", build)


@cli.command("auth")
def run_auth(
    conf: str = Option(None, help="Path to .env file with configuration"),  # noqa: B008
    build: bool = Option(False, help="Whether to skip build step"),  # noqa: B008
) -> None:
    run_kolombo_component("auth", build)


@cli.command("nginx")
def run_nginx(
    conf: str = Option(None, help="Path to .env file with configuration"),  # noqa: B008
    build: bool = Option(False, help="Whether to skip build step"),  # noqa: B008
) -> None:
    run_kolombo_component("nginx", build)


async def _run_senders(build: bool) -> None:
    log = CliLog()
    domains = {domain.actual for domain in await Domain.all_active()}
    if len(domains) < 1:
        log.error("No active domains to run senders for. Aborting")
        exit(0)

    if build or not kolombo_image_exists(component="sender"):
        log.step("- Building kolombo-sender")
        build_kolombo_image(component="sender")

    log.step("- Creating kolombo network (if does not exist)")
    create_network("kolombo", subnet="192.168.79.0/24")

    for domain in domains:
        log.step(f"- Running kolombo-sender container for {domain}")
        run_container(
            "kolombo-sender",
            args=domain,
            name=f"kolombo-{domain}-sender",
            net="kolombo",
            volumes=["/etc/kolombo/dkim_keys:/etc/opendkim/keys"],
            # Attach TTY and run in background
            other_flags="-t -d",
        )


@cli.command("senders")
@async_command
async def run_senders(
    conf: str = Option(None, help="Path to .env file with configuration"),  # noqa: B008
    build: bool = Option(False, help="Whether to skip build step"),  # noqa: B008
) -> None:
    await _run_senders(build)


@cli.command("all")
@async_command
async def run_all(
    conf: str = Option(None, help="Path to .env file with configuration"),  # noqa: B008
    build: bool = Option(False, help="Whether to skip build step"),  # noqa: B008
) -> None:
    run_kolombo_component("receiver", build)
    await _run_senders(build)
    run_kolombo_component("auth", build)
    run_kolombo_component("nginx", build)
