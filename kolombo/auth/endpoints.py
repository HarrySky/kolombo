from email.utils import parseaddr

from fastapi import Header, Response

from kolombo import conf
from kolombo.auth._resolver import get_ip_by_host
from kolombo.auth.credentials import check_credentials
from kolombo.auth.protocol import AuthError, AuthSuccess
from kolombo.models import Domain
from kolombo.resources import log

#: We only put SMTP-send and IMAP behind auth, POP3 is unsupported (and old)
_protocol_to_port_mapping = {"smtp": 25, "imap": 143}


async def auth(
    x_secret_key: str = Header(...),  # noqa: B008
    domain: str = Header(..., alias="X-Domain"),  # noqa: B008
    protocol: str = Header(..., alias="Auth-Protocol"),  # noqa: B008
    auth_method: str = Header(...),  # noqa: B008
    email: str = Header(..., alias="Auth-User"),  # noqa: B008
    password: str = Header(..., alias="Auth-Pass"),  # noqa: B008
    login_attempt: int = Header(..., alias="Auth-Login-Attempt"),  # noqa: B008
    client_ip: str = Header(...),  # noqa: B008
) -> Response:
    """Endpoint used for auth of SMTP/IMAP users."""
    if x_secret_key != conf.NGINX_SECRET_KEY:
        # This MUST NOT happen if everything is set up properly
        log.error("Not nginx trying to use API")
        return AuthError("Go Away", retry=False)

    # Check for possible usage errors to close connection early
    if protocol not in _protocol_to_port_mapping:
        return AuthError("Unsupported protocol", retry=False)
    elif auth_method != "plain":
        return AuthError("Unsupported auth method", retry=False)

    # Remove newline from credentials
    email = email.rstrip("%0A")
    password = password.rstrip("%0A")
    if not await check_credentials(email, password, domain):
        log.warning("Failed %s auth as %s from %s", protocol, email, client_ip)
        retry = login_attempt < conf.MAX_ATTEMPTS
        return AuthError("Invalid login or password", retry=retry)

    log.info("Successful %s auth as %s from %s", protocol, email, client_ip)
    server_host = "kolombo-receiver"
    if protocol == "smtp":
        server_host = f"kolombo-{domain}-sender"

    server_ip = get_ip_by_host(server_host)
    server_port = _protocol_to_port_mapping[protocol]
    log.debug("Forwarding nginx to %s:%s (%s)", server_ip, server_port, server_host)
    return AuthSuccess(server_ip, server_port)


async def receive(
    x_secret_key: str = Header(...),  # noqa: B008
    protocol: str = Header(..., alias="Auth-Protocol"),  # noqa: B008
    smtp_from: str = Header(..., alias="Auth-SMTP-From"),  # noqa: B008
    client_ip: str = Header(...),  # noqa: B008
) -> Response:
    """Endpoint used for receiving SMTP without authentication."""
    if x_secret_key != conf.NGINX_SECRET_KEY:
        # This MUST NOT happen if everything is set up properly
        log.error("Not nginx trying to use API")
        return AuthError("Go Away", retry=False)

    if protocol != "smtp":
        # This MUST NOT happen if everything is set up properly
        log.error("Not SMTP protocol in receive endpoint")
        return AuthError("Go Away", retry=False)

    parsed_smtp_from = parseaddr(smtp_from)
    email = parsed_smtp_from[1]
    if parsed_smtp_from == ("", "") or email.count("@") != 1:
        log.debug("Bad email address rejected: %s", smtp_from)
        return AuthError("Bad Email Address", retry=False, error_code="510")

    # TODO: Implement spam/ignore list check here (?)

    domain = email.split("@")[1]
    is_our_domain = await Domain.objects.filter(actual=domain, active=True).exists()
    # Our domain, but not from kolombo-sender container? Not letting it through
    if is_our_domain and client_ip != get_ip_by_host(f"kolombo-{domain}-sender"):
        log.warning("Impersonation attempt (%s) from %s", email, client_ip)
        return AuthError("Use 587 Port", retry=False)

    log.info("Receiving email from IP %s (%s)", client_ip, smtp_from)
    server_ip = get_ip_by_host("kolombo-receiver")
    log.debug("Forwarding nginx to %s:25 (kolombo-receiver)", server_ip)
    return AuthSuccess(server_ip, 25)
