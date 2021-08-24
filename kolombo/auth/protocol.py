"""
Responses that API MUST return, according to nginx mail auth protocol:
https://nginx.org/en/docs/mail/ngx_mail_auth_http_module.html#protocol
"""
from fastapi import Response


class AuthSuccess(Response):
    """
    Response that MUST be returned after successful auth.

    Parameters:

    * server_ip - IP that nginx will use to access real SMTP/IMAP server.
    * server_port - port that nginx will use to access real SMTP/IMAP server.
    """

    def __init__(self, server_ip: str, server_port: int) -> None:
        headers = {
            "Auth-Status": "OK",
            "Auth-Server": server_ip,
            "Auth-Port": str(server_port),
        }
        super().__init__(content=None, status_code=200, headers=headers)


class AuthError(Response):
    """
    Response that MUST be returned when auth error occured.

    Parameters:

    * status - status that explains error that happened.
    * retry - *(optional)* whether client can retry (default behaviour)
    or connection will be closed.
    * wait - *(optional)* seconds to wait if client can retry (default - 2).
    * error_code - *(optional)* error code that will be used in SMTP case
    (default - "535 5.7.0", a.k.a. "Authentication Failed").
    """

    def __init__(
        self,
        status: str,
        *,
        retry: bool = True,
        wait: int = 2,
        error_code: str = "535 5.7.0",
    ) -> None:
        if status == "OK":
            raise ValueError("Status MUST NOT be 'OK' in error headers")

        headers = {"Auth-Status": status, "Auth-Error-Code": error_code}
        if retry:
            headers["Auth-Wait"] = str(wait)

        super().__init__(content=None, status_code=200, headers=headers)
