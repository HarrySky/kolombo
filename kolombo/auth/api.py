from fastapi import FastAPI

from kolombo import conf
from kolombo.auth.endpoints import auth
from kolombo.models import init_database

conf.read_configuration()
app = FastAPI(
    title="Kolombo auth API",
    debug=conf.DEBUG,
    on_startup=[init_database],
    # Disable Swagger UI and other API docs
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
)
app.add_api_route("/auth", auth, methods=["GET"])
