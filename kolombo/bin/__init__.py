from os import path

from typer import Context, Typer

from kolombo import conf
from kolombo.console import error
from kolombo.dkim import dkim_cli
from kolombo.domain import domain_cli
from kolombo.init import init
from kolombo.run import run_cli
from kolombo.stop import stop_cli
from kolombo.user import user_cli

kolombo_cli = Typer(name="kolombo", add_completion=True)
kolombo_cli.command("init")(init)
kolombo_cli.add_typer(domain_cli, name="domain")
kolombo_cli.add_typer(dkim_cli, name="dkim")
kolombo_cli.add_typer(user_cli, name="user")
kolombo_cli.add_typer(run_cli, name="run")
kolombo_cli.add_typer(stop_cli, name="stop")


@kolombo_cli.callback()
def main(ctx: Context) -> None:
    if ctx.invoked_subcommand == "init":
        return

    if not path.exists("/etc/kolombo/kolombo.conf"):
        error("Kolombo is not initialized! Run [code]kolombo init[/] first")
        exit(1)

    conf.read_configuration()
