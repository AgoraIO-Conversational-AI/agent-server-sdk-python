import hashlib
import hmac
import struct
import time
import typing

DEFAULT_EXPIRY_SECONDS = 3600


class GenerateTokenOptions(typing.TypedDict, total=False):
    app_id: str
    app_certificate: str
    channel: str
    uid: int
    role: int
    expiry_seconds: int


ROLE_PUBLISHER = 1
ROLE_SUBSCRIBER = 2

_VERSION = "007"
_APP_ID_LENGTH = 32


def _pack_uint16(value: int) -> bytes:
    return struct.pack("<H", value)


def _pack_uint32(value: int) -> bytes:
    return struct.pack("<I", value)


def _pack_string(value: str) -> bytes:
    encoded = value.encode("utf-8")
    return _pack_uint16(len(encoded)) + encoded


def _pack_map(m: typing.Dict[int, int]) -> bytes:
    result = _pack_uint16(len(m))
    for k, v in sorted(m.items()):
        result += _pack_uint16(k) + _pack_uint32(v)
    return result


def _generate_dynamic_key(
    app_id: str,
    app_certificate: str,
    channel: str,
    uid: int,
    privilege_expire_ts: int,
) -> str:
    token_expire_ts = privilege_expire_ts

    privileges: typing.Dict[int, int] = {}
    privileges[1] = privilege_expire_ts
    privileges[2] = privilege_expire_ts

    message = _pack_uint32(0)
    message += _pack_uint32(int(time.time()))
    message += _pack_uint32(token_expire_ts)
    message += _pack_map(privileges)

    signing_key = hmac.new(
        app_certificate.encode("utf-8"),
        app_id.encode("utf-8"),
        hashlib.sha256,
    ).digest()

    content = _pack_string(app_id)
    content += _pack_uint32(int(time.time()))
    content += message

    signature = hmac.new(signing_key, content, hashlib.sha256).digest()

    import base64

    content_b64 = base64.b64encode(content).decode("utf-8")
    signature_b64 = base64.b64encode(signature).decode("utf-8")
    message_b64 = base64.b64encode(message).decode("utf-8")

    return f"{_VERSION}{signature_b64}{content_b64}{message_b64}"


def generate_rtc_token(
    app_id: str,
    app_certificate: str,
    channel: str,
    uid: int,
    role: int = ROLE_PUBLISHER,
    expiry_seconds: int = DEFAULT_EXPIRY_SECONDS,
) -> str:
    """Build a short-lived RTC token.

    Both token_expire and privilege_expire are set to the same value.

    Parameters
    ----------
    app_id : str
        Agora App ID.
    app_certificate : str
        Agora App Certificate.
    channel : str
        Channel name.
    uid : int
        User ID.
    role : int
        RTC role (ROLE_PUBLISHER or ROLE_SUBSCRIBER).
    expiry_seconds : int
        Token expiry in seconds (default 3600).

    Returns
    -------
    str
        The generated RTC token.
    """
    try:
        from agora_token_builder import RtcTokenBuilder  # type: ignore[import-not-found]

        privilege_expire_ts = int(time.time()) + expiry_seconds
        return RtcTokenBuilder.buildTokenWithUid(
            app_id,
            app_certificate,
            channel,
            uid,
            role,
            privilege_expire_ts,
        )
    except ImportError:
        privilege_expire_ts = int(time.time()) + expiry_seconds
        return _generate_dynamic_key(
            app_id,
            app_certificate,
            channel,
            uid,
            privilege_expire_ts,
        )
