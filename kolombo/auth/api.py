from fastapi import FastAPI

from kolombo import conf
from kolombo.auth.endpoints import auth
from kolombo.resources import init_database, init_logger

api = FastAPI(
    debug=conf.DEBUG,
    on_startup=[init_logger, init_database],
    # Disable Swagger UI and other docs
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
)
api.add_api_route("/auth", auth, methods=["GET"])
