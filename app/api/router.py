import random
import time

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from yarl import URL

from app.request_check import verify_request_source
from utils.config import get_config
from utils.openlist import sign as openlist_sign

router = APIRouter()


@router.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="https://ghacg.com", status_code=302)


@router.get("/d/{path:path}", dependencies=[Depends(verify_request_source)])
def redirect(path: str) -> RedirectResponse:
    cfg = get_config()
    expire = int(time.time()) + 3600
    sign_value = openlist_sign(f"/{path}", cfg.sign_token, expire)
    base = URL(random.choice(cfg.fs_base))
    target = (base / path).with_query(sign=sign_value)
    return RedirectResponse(url=str(target), status_code=302)
