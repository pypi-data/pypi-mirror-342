import datetime

import jwt
from django.conf import settings


def get_aws_connect_jwt(widget_id: str, expires_in: int = 500) -> str:
    if expires_in > 600:
        raise ValueError(f"'expires_in' must be less than 600, got '{expires_in}'.")

    payload = {
        "sub": widget_id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() - datetime.timedelta(seconds=expires_in),
        "segmentAttributes": {"connect:Subtype": {"ValueString": "connect:Guide"}},
    }
    header = {"typ": "JWT", "alg": "HS256"}
    encoded_token = jwt.encode(
        payload, settings.CONNECT_SECRET, algorithm=header["alg"], headers=header
    )
    return encoded_token
