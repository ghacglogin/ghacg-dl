from fastapi import FastAPI

from app.api.router import router
from app.exceptions.handlers import register_exception_handlers

app = FastAPI()
register_exception_handlers(app)
app.include_router(router)
