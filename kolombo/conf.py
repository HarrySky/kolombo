from typing import Dict

from kolombo.console import enable_debug

#: Whether debug mode is enabled
DEBUG: bool = False
#: Secret key that is sent in X-Secret-Key header from nginx
NGINX_SECRET_KEY: str = "changeme"
#: Maximum number of auth attempts before API closes connection with client
MAX_ATTEMPTS: int = 3
#: Salt used for passwords hashing
SALT: bytes = b"changeme"
#: URL used to connect to database
DATABASE_URL: str = "sqlite:////etc/kolombo/kolombo.sqlite"


def _read_config_file(config_path: str) -> Dict[str, str]:
    """Copied from starlette.config.Config"""
    config: Dict[str, str] = {}
    with open(config_path) as config_file:
        for line in config_file.readlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip("\"'")
                config[key] = value

    return config


def read_configuration() -> None:
    config = _read_config_file("/etc/kolombo/kolombo.conf")

    global DEBUG
    DEBUG = bool(config.get("DEBUG", False))
    if DEBUG:
        enable_debug()

    global NGINX_SECRET_KEY
    NGINX_SECRET_KEY = config.get("NGINX_SECRET_KEY", "changeme")

    global MAX_ATTEMPTS
    MAX_ATTEMPTS = int(config.get("MAX_ATTEMPTS", 3))

    global SALT
    SALT = config.get("SALT", "changeme").encode("utf-8")
