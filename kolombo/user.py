from base64 import b64encode
from typing import TYPE_CHECKING, List

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from typer import Argument, Typer, prompt

from kolombo.console import error, finished, info, print_list, started, step, warning
from kolombo.util import async_command, needs_database

if TYPE_CHECKING:
    from kolombo.models import User

user_cli = Typer()


@user_cli.command("list")
@async_command
@needs_database
async def list_users() -> None:
    from kolombo.models import User

    active_users = [user.email for user in await User.all_active()]
    info(f"Active users: {len(active_users)}")
    if len(active_users) > 0:
        print_list(active_users)


async def _save_user(email: str, password: str, domain: str) -> None:
    from kolombo import conf
    from kolombo.models import User

    kdf = Scrypt(conf.SALT, length=32, n=2 ** 16, r=8, p=1)
    b64_password = b64encode(kdf.derive(password.encode("utf-8")))
    await User.objects.create(email=email, password=b64_password, domain=domain)


def update_virtual_files(active_users: List["User"]) -> None:
    emails = [user.email for user in active_users]
    addresses = "\n".join(f"{email} {email}" for email in emails)
    with open("/etc/kolombo/virtual/addresses", mode="w") as addresses_file:
        addresses_file.write(f"{addresses}\n")

    mailboxes = "\n".join(f"{email} {email}/" for email in emails)
    with open("/etc/kolombo/virtual/mailbox", mode="w") as mailbox_file:
        mailbox_file.write(f"{mailboxes}\n")


@user_cli.command("add")
@async_command
@needs_database
async def add_user(
    email: str = Argument(..., help="Email for new user"),  # noqa: B008
) -> None:
    from kolombo.models import Domain, User

    if "@" not in email:
        error(f"Email '{email}' does not contain '@'!")
        exit(1)

    domain = email.split("@", maxsplit=1)[1].strip()
    if not domain:
        error("Domain part MUST NOT be empty string!")
        exit(1)
    elif not await Domain.objects.filter(active=True, actual=domain).exists():
        error(f"Domain '{domain}' is not added (or inactive)!")
        warning(
            f"You can add it via [code]kolombo domain add {domain} mx.{domain}[/code]"
        )
        exit(1)
    elif await User.objects.filter(email=email).exists():
        error(f"User with email '{email}' already exists!")
        exit(1)

    started(f"Adding [code]{email}[/] user")

    password = prompt(f"{email} password", hide_input=True, confirmation_prompt=True)
    step("Saving to database")
    await _save_user(email, password, domain)

    step("Updating virtual files (addresses and mailbox map)")
    active_users = await User.all_active()
    update_virtual_files(active_users)

    warning("Run command [code]kolombo run[/] to reload Kolombo")

    finished(f"User '{email}' added!")
