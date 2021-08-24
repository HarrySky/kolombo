from os import path

from docker import from_env  # type: ignore[import]
from typer import Argument, Typer

from kolombo.console import error, info, step
from kolombo.util import build_kolombo_image, execute_as_root

dkim_cli = Typer()


def read_dkim_txt_record(domain: str) -> str:
    with open(f"/etc/kolombo/dkim_keys/{domain}.txt", mode="r") as txt_file:
        txt_file_content = txt_file.read()

    paren_open_idx = txt_file_content.find("(")
    paren_close_idx = txt_file_content.find(")")
    txt_record = txt_file_content[paren_open_idx + 1 : paren_close_idx]  # noqa: E203
    return txt_record.replace('"\n\t  "', "")


@dkim_cli.command("generate")
@execute_as_root
def generate_keys(
    domain: str = Argument(..., help="Domain to generate DKIM keys for"),  # noqa: B008
) -> None:
    client = from_env()
    build_kolombo_image(client, "dkim-gen")

    step(f"Generating DKIM keys for domain: {domain}")
    client.containers.run(
        "kolombo-dkim-gen",
        domain,
        stderr=True,
        auto_remove=True,
        volumes=["/etc/kolombo/dkim_keys:/etc/opendkim/keys"],
    )

    dkim_txt = read_dkim_txt_record(domain)
    info(f"[b]TXT[/] record for [b u]mail._domainkey.{domain}[/] is: {dkim_txt}")


@dkim_cli.command("txt")
@execute_as_root
def get_txt_record(
    domain: str = Argument(  # noqa: B008
        ..., help="Domain to get DKIM TXT record for (if it was generated)"
    ),
) -> None:
    if not path.exists(f"/etc/kolombo/dkim_keys/{domain}.txt"):
        error(f"There is no DKIM TXT record generated for {domain}!")
        exit(1)

    dkim_txt = read_dkim_txt_record(domain)
    info(f"[b]TXT[/] record for [b u]mail._domainkey.{domain}[/] is: {dkim_txt}")
