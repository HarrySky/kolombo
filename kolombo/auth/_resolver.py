from socket import gethostbyname


def get_ip_by_host(host: str) -> str:
    """Return IP address for provided host (fast in Docker network)"""
    return gethostbyname(host)
