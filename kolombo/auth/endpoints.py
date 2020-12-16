from fastapi import Header, Response

from kolombo import conf
from kolombo.auth._resolver import get_ip_by_host
from kolombo.auth.credentials import check_credentials
from kolombo.auth.protocol import AuthError, AuthSuccess
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
