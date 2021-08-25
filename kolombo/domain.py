from typing import TYPE_CHECKING, List

from typer import Argument, Typer

from kolombo.configuration_files import (
    generate_nginx_config,
    generate_virtual_domains,
    generate_virtual_ssl_map,
)
from kolombo.console import error, finished, info, print_list, started, step, warning
from kolombo.util import async_command, needs_database

if TYPE_CHECKING:
    from kolombo.models import Domain

domain_cli = Typer()


@domain_cli.command("list")
@async_command
@needs_database
async def list_domains() -> None:
    from kolombo.models import Domain

    all_domains = await Domain.all_active()
    active_pairs = [f"(MX) {domain.mx} -> {domain.actual}" for domain in all_domains]
    info(f"Active domains: {len(active_pairs)}")
    if len(active_pairs) > 0:
        print_list(active_pairs)


def update_virtual_files(active_domains: List["Domain"]) -> None:
    domains = (domain.actual for domain in active_domains)
    virtual_domains = generate_virtual_domains(domains)
    with open("/etc/kolombo/virtual/domains", mode="w") as virtual_domains_file:
        virtual_domains_file.write(f"{virtual_domains}\n")

    mx_domains = (domain.mx for domain in active_domains)
    virtual_ssl_map = generate_virtual_ssl_map(mx_domains)
    with open("/etc/kolombo/virtual/ssl_map", mode="w") as virtual_ssl_map_file:
        virtual_ssl_map_file.write(f"{virtual_ssl_map}\n")


@domain_cli.command("add")
@async_command
@needs_database
async def add_domain(
    domain: str = Argument(  # noqa: B008
        ..., help="Domain that comes after @ in email"
    ),
    mx: str = Argument(None, help="Domain from DNS MX record if exists"),  # noqa: B008
) -> None:
    from kolombo import conf
    from kolombo.models import Domain

    if mx is None:
        mx = domain

    if not domain or not mx:
        error("Arguments MUST NOT be empty strings!")
        exit(1)
    elif await Domain.objects.filter(actual=domain, mx=mx).exists():
        error(f"Pair [code]{mx} -> {domain}[/] already exists!")
        exit(1)

    started(f"Adding [code]{mx} -> {domain}[/] pair")

    step("Adding configuration to [code]mail-enabled[/]")
    nginx_config = generate_nginx_config(mx, domain, conf.NGINX_SECRET_KEY)
    with open(f"/etc/kolombo/mail-enabled/{mx}.conf", mode="w") as nginx_file:
        nginx_file.write(nginx_config)

    step("Saving to database")
    await Domain.objects.create(actual=domain, mx=mx)

    step("Updating virtual files (domains and SSL map)")
    active_domains = await Domain.all_active()
    update_virtual_files(active_domains)

    warning(
        f"Run command [code]kolombo dkim generate {domain}[/] to generate DKIM keys"
    )
    warning("Run command [code]kolombo run[/] to reload Kolombo")

    finished(f"Pair [code]{mx} -> {domain}[/] added!")
