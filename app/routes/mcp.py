"""MCP handshake route

Provides a simple MCP discovery endpoint at /mcp.
Optionally validates an Authorization: Bearer <base64(phone)> header
and echoes the authenticated phone in the response.

This is a lightweight contract for Puch AI's MCP client to
programmatically discover available tools and confirm connectivity.
"""

from fastapi import APIRouter, Header
from typing import Optional

# Reuse token logic from auth route
try:
    from .auth import _extract_phone_from_token
except Exception:
    # Fallback no-op if auth not available
    def _extract_phone_from_token(token: str) -> str:
        return ""

router = APIRouter()


@router.get("/mcp", summary="MCP discovery and handshake")
def mcp_root(authorization: Optional[str] = Header(None, alias="Authorization")):
    phone = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
        try:
            phone = _extract_phone_from_token(token)
        except Exception:
            # Keep phone as None on invalid token; endpoint still returns 200 for discovery
            phone = None

    return {
        "name": "Desi Food MCP",
        "version": "1.0.0",
        "status": "ok",
        "tools": [
            {
                "name": "get_recipe",
                "method": "GET",
                "path": "/get_recipe",
                "params": ["user_id", "dish"],
            },
            {
                "name": "recommend",
                "method": "GET",
                "path": "/recommend",
                "params": ["keyword", "diet", "course", "top_n"],
            },
            {
                "name": "validate",
                "method": "GET",
                "path": "/validate",
                "auth": "Bearer Base64(phone)",
            },
        ],
        "auth": {
            "type": "bearer_base64_phone",
            "validate_path": "/validate",
            "phone": phone,
        },
    }
