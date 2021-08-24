from socket import gethostbyname


def get_ip_for_host(host: str) -> str:
    """Return IP address for provided host (fast in Docker network)"""
    return gethostbyname(host)
