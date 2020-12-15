from base64 import b64decode

from cryptography.exceptions import InvalidKey
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from ormar.exceptions import NoMatch

from kolombo import conf
from kolombo.models import User
from kolombo.resources import log


async def check_credentials(email: str, password: str, domain: str) -> bool:
    key_material = password.encode("utf-8")
    try:
        user = await User.objects.filter(active=True, email=email, domain=domain).get()
        expected_key = b64decode(user.password)
    except NoMatch:
        log.debug("No active user '%s' from domain '%s' found", email, domain)
        key_material = b"Password that 100% not matching, I swear"
        expected_key = b"Password that 100% not matching, trust me"

    kdf = Scrypt(conf.SALT, length=32, n=2 ** 16, r=8, p=1)  # type: ignore[call-arg]
    try:
        kdf.verify(key_material, expected_key)
        return True
    except InvalidKey:
        return False
