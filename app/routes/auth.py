"""Auth routes: /validate endpoint

This provides a simple bearer-token validation that extracts a phone
number from the token.  For the MVP we treat the token payload as a
Base64-encoded string containing the full phone number (e.g.
"OTk4NzY1NDMyMTA=" → "99876543210").

In production you would swap this logic out for a real JWT/OAuth
validator that checks signatures, expiry, issuer, etc.
"""

from fastapi import APIRouter, Header, HTTPException, status
import base64
import re

router = APIRouter()

PHONE_REGEX = re.compile(r"^\d{10,15}$")  # e.g. 919876543210


def _extract_phone_from_token(token: str) -> str:
    """Decode Base64 token and return phone number string if valid."""
    try:
        decoded = base64.b64decode(token).decode()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: cannot decode",
        ) from exc

    decoded = decoded.strip()
    if not PHONE_REGEX.match(decoded):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: phone format",
        )
    return decoded


@router.get("/validate", summary="Validate bearer token and return phone number")
def validate_token(authorization: str = Header(..., alias="Authorization")):
    """Validate a bearer token and return the authenticated phone number.

    The endpoint expects an **Authorization** header of the form:

        Authorization: Bearer <token>

    where `<token>` is a Base64-encoded phone number.  On success the
    response is:

        {"phone": "919876543210"}
    """
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Bearer token",
        )

    token = authorization.split(" ", 1)[1].strip()
    phone = _extract_phone_from_token(token)
    return {"phone": phone}
