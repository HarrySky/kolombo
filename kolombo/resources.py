from logging import DEBUG, INFO, Formatter, StreamHandler, getLogger

from databases import Database
from sqlalchemy import MetaData, create_engine  # type: ignore[import]

from kolombo import conf

database = Database(conf.DATABASE_URL)
metadata = MetaData()
log = getLogger("kolombo")


def init_logger() -> None:
    log.setLevel(DEBUG if conf.DEBUG else INFO)
    formatter = Formatter("%(asctime)s [kolombo:%(levelname)s] %(message)s")
    stderr_handler = StreamHandler()
    stderr_handler.setFormatter(formatter)
    log.addHandler(stderr_handler)


async def init_database() -> None:
    await database.connect()
    engine = create_engine(conf.DATABASE_URL)
    metadata.create_all(engine)
