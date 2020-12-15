from os import environ

from typer import Typer

from kolombo.bin.domain import cli as domain_cli
from kolombo.bin.run import cli as run_cli
from kolombo.bin.user import cli as user_cli
from kolombo.bin.util import CliLog, run_command

cli = Typer()
cli.add_typer(user_cli, name="user")
cli.add_typer(domain_cli, name="domain")
cli.add_typer(run_cli, name="run")
#: Default content of /etc/kolombo/kolombo.env file
_default_env = """# This is configuration file for kolombo that is used by default
# To enable debug - change to 1 here
DEBUG=0
# Secret key that is used to determine that nginx is using API
# NB! Change this secret!
NGINX_SECRET_KEY=changeme
# Maximum auth attempts
MAX_ATTEMPTS=3
# Salt used for passwords hashing
# NB! Change this secret!
SALT=changeme
# Name of SQLite database file
DATABASE_NAME=kolombo
"""
#: Default content of /etc/kolombo/virtual/ files
_virtual = {
    "addresses": "bob@example.com bob@example.com",
    "domains": "example.com",
    "mailbox": "bob@example.com bob@example.com/",
}


@cli.command("setup")
def setup() -> None:
    """Set up kolombo for current user"""
    log = CliLog()
    log.step("- Installing bash completion")
    run_command("kolombo --install-completion bash")

    log.step("- Creating /etc/kolombo folders and files")
    log.step("-- Creating /etc/kolombo folder (using sudo)")
    run_command("mkdir -p -m 770 /etc/kolombo", sudo=True)

    user = environ["USER"]
    log.step(f"-- Setting /etc/kolombo owner to {user} (using sudo)")
    run_command(f"chown {user}:{user} /etc/kolombo", sudo=True)

    log.step("-- Creating /etc/kolombo folders for volumes")
    run_command("mkdir -p -m 770 /etc/kolombo/maildirs")
    run_command("mkdir -p -m 770 /etc/kolombo/mail-enabled")
    run_command("mkdir -p -m 770 /etc/kolombo/virtual")
    run_command("mkdir -p -m 700 /etc/kolombo/dkim_keys")

    log.step("-- Writing default conf to /etc/kolombo/kolombo.env")
    with open("/etc/kolombo/kolombo.env", "w") as default_config:
        default_config.write(_default_env)

    for file in ("addresses", "domains", "mailbox"):
        log.step(f"-- Writing default file to /etc/kolombo/virtual/{file}")
        with open(f"/etc/kolombo/virtual/{file}", "w") as virtual_file:
            virtual_file.write(f"{_virtual[file]}\n")


def main() -> None:
    cli()
