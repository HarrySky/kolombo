import sys
from os import R_OK, access, path
from warnings import warn

from starlette.config import Config

_config_file = "/etc/kolombo/kolombo.env"
if "--conf" in sys.argv:
    _config_file = sys.argv[sys.argv.index("--conf") + 1]

if not path.exists(_config_file) or not access(_config_file, R_OK):
    warn(f"Config file ({_config_file}) does not exist or not readable", UserWarning)

_config = Config(env_file=_config_file)
#: Whether debug is enabled
DEBUG: bool = _config.get("DEBUG", bool, False)
#: Secret key that should be sent in X-Secret-Key header from nginx
NGINX_SECRET_KEY: str = _config.get("NGINX_SECRET_KEY", str, "changeme")
#: Max number of attempts before API closes connection with client
MAX_ATTEMPTS: int = _config.get("MAX_ATTEMPTS", int, 3)
#: Salt used for passwords hashing
SALT: bytes = _config.get("SALT", str, "changeme").encode("utf-8")
#: Name of database file without extension
DATABASE_NAME: str = _config.get("DATABASE_NAME", str, "kolombo")
#: URL used to connect to database
DATABASE_URL = f"sqlite:////etc/kolombo/{DATABASE_NAME}.sqlite"
