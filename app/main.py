from fastapi import FastAPI

from app.api.router import router
from app.exceptions.handlers import register_exception_handlers
from app.settings import is_production

if is_production():
    app = FastAPI(
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        title="",
        description="",
        version="",
    )
else:
    app = FastAPI()

register_exception_handlers(app)
app.include_router(router)
