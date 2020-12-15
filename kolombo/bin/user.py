from base64 import b64encode

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from rich.markdown import Markdown
from typer import Argument, Option, Typer, prompt

from kolombo import conf
from kolombo.bin.util import CliLog, async_command
from kolombo.models import Domain, User
from kolombo.resources import init_database

cli = Typer()


@cli.command("list")
@async_command
async def list_users(
    conf: str = Option(None, help="Path to .env file with configuration")  # noqa: B008
) -> None:
    log = CliLog()
    await init_database()

    active_users = [user.email for user in await User.all_active()]
    log.step(f"Active users: {len(active_users)}")
    if len(active_users) > 0:
        log.info(Markdown(f"*  {'* '.join(active_users)}"))


async def _add_user(email: str, password: str, domain: str) -> None:
    kdf = Scrypt(conf.SALT, length=32, n=2 ** 16, r=8, p=1)  # type: ignore[call-arg]
    b64_password = b64encode(kdf.derive(password.encode("utf-8")))
    await User.objects.create(email=email, password=b64_password, domain=domain)


async def _update_virtual_files() -> None:
    emails = [user.email for user in await User.all_active()]
    addresses = "\n".join(f"{email} {email}" for email in emails)
    with open("/etc/kolombo/virtual/addresses", mode="w") as addresses_file:
        addresses_file.write(f"{addresses}\n")

    mailboxes = "\n".join(f"{email} {email}/" for email in emails)
    with open("/etc/kolombo/virtual/mailbox", mode="w") as mailbox_file:
        mailbox_file.write(f"{mailboxes}\n")


@cli.command("add")
@async_command
async def add_user(
    conf: str = Option(None, help="Path to .env file with configuration"),  # noqa: B008
    email: str = Argument(..., help="Email for new user"),  # noqa: B008
) -> None:
    log = CliLog()
    await init_database()

    if "@" not in email:
        log.error(f"Email '{email}' does not contain @")
        exit(1)

    domain = email.split("@", maxsplit=1)[1].strip()
    if not domain:
        log.error("Domain part MUST NOT be empty string")
        exit(2)
    elif not await Domain.objects.filter(active=True, actual=domain).exists():
        log.error(
            f"Domain '{domain}' is not added, you can add it via "
            f"[code]kolombo domain add {domain} mx.{domain}[/code]",
        )
        exit(3)
    elif await User.objects.filter(email=email).exists():
        log.error(f"User with email '{email}' exists")
        exit(4)

    password = prompt(f"{email} password", hide_input=True, confirmation_prompt=True)
    await _add_user(email, password, domain)
    await _update_virtual_files()
    # TODO: Do postfix reload in kolombo-receiver
    log.step(f"User '{email}' added!")
