"""请求来源校验。

校验三件事：
1. Referer 在白名单内；
2. User-Agent 不在黑名单内；
3. ``dl_session`` Cookie 由主站签发且未过期。

``dl_session`` 的 Cookie 值格式为 ``"<timestamp>|<hex_signature>"``，
其中 ``hex_signature = HMAC_SHA256(secret, str(timestamp))``。
仅用作防盗链令牌，不绑定 IP / 用户身份。
"""

from __future__ import annotations

import hmac
import time
from hashlib import sha256
from typing import Annotated
from urllib.parse import unquote

from fastapi import Cookie, Header

from utils.config import get_config
from utils.exceptions import (
    CookieCheckFailedException,
    IllegalRefererException,
    IllegalUserAgentException,
)


def verify_session(dl_session: str) -> bool:
    """校验 ``dl_session`` Cookie 是否合法且在有效期内。"""
    cfg = get_config()
    secret = cfg.dl_session_secret
    if not secret:
        # 未配置密钥时拒绝放行，避免静默降级
        return False

    # 浏览器/下发端会对 cookie value 中的 "|" 做 percent-encoding（%7C），
    # 而 Starlette 的 Cookie 解析不会自动 unquote，需要先还原再切分。
    parts = unquote(dl_session).split("|", 1)
    if len(parts) != 2:
        return False
    ts_str, sig_hex = parts

    if not ts_str.isdigit():
        return False
    ts = int(ts_str)

    now = int(time.time())
    # 允许 30 秒时钟偏移；超过 max_age 视为过期
    if ts > now + 30 or now - ts > cfg.dl_session_max_age:
        return False

    expected = hmac.new(
        secret.encode("utf-8"),
        ts_str.encode("ascii"),
        sha256,
    ).hexdigest()

    # 长度不一致时 compare_digest 也会安全返回 False，但提前过滤减少计算
    if len(sig_hex) != len(expected):
        return False
    return hmac.compare_digest(sig_hex, expected)


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

    if dl_session is None or not verify_session(dl_session):
        raise CookieCheckFailedException()
