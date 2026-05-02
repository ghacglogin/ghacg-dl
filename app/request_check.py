from typing import Annotated

from fastapi import FastAPI, Header, Cookie

from utils.exceptions import IllegalRefererException, IllegalUserAgentException, CookieCheckFailedException
from utils.config import get_config

def verify_session(dl_session: str) -> None:
    return True

async def verify_request_source(
    referer: Annotated[str | None, Header()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    dl_session: Annotated[str | None, Cookie()] = None,
) -> None:
    cfg = get_config()
    if referer is None:
        raise IllegalRefererException()
    for allowed_referrer in cfg.allowed_referrers:
        if allowed_referrer in referer:
            break
    else:
        raise IllegalRefererException()
    if user_agent is None:
        raise IllegalUserAgentException()
    for ua_blacklist in cfg.ua_blacklist:
        if ua_blacklist in user_agent:
            raise IllegalUserAgentException()
    
    if dl_session is not None:
        if verify_session(dl_session):
            return
        else:
            raise CookieCheckFailedException()
    else:
        raise CookieCheckFailedException()
    