import time
import secrets
import httpx
from fastapi import HTTPException, Header
from jose import jwt, JWTError
from .config import settings


# In-memory challenge store (swap for Redis later)
challenge_store = {}
_cached_keys = {}
_last_fetched = 0


def generate_client_challenge(device_id: str) -> str:
    """Create a unique challenge tied to a device ID"""
    challenge = secrets.token_urlsafe(32)
    challenge_store[challenge] = {
        "device_id": device_id,
        "timestamp": time.time()
    }
    return challenge

def validate_challenge(challenge: str, device_id: str) -> bool:
    """Check that the challenge exists, is fresh, and matches device"""
    data = challenge_store.get(challenge)
    if not data:
        return False
    if time.time() - data["timestamp"] > settings.CHALLENGE_EXPIRY_SECONDS:
        challenge_store.pop(challenge, None)
        return False
    if data["device_id"] != device_id:
        return False
    challenge_store.pop(challenge, None)  # Invalidate challenge to prevent replay
    return True

def issue_attested_session_token(device_id: str) -> str:
    payload = {
        "device_id": device_id,
        "iat": int(time.time()),
        "exp": int(time.time()) + settings.JWT_EXPIRY_SECONDS,
        "type": "attested_session"
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

async def get_apple_public_keys():
    global _cached_keys, _last_fetched
    if time.time() - _last_fetched > 3600:
        async with httpx.AsyncClient() as client:
            resp = await client.get(settings.APPLE_PUBLIC_KEYS_URL)
            resp.raise_for_status()  # raise if non-200 response
            _cached_keys = resp.json()
            _last_fetched = time.time()
    return _cached_keys.get("keys", [])

async def verify_attestation_token(token: str, expected_device_id: str, expected_challenge: str):
    keys = await get_apple_public_keys()
    for key in keys:
        try:
            payload = jwt.decode(
                token,
                key,
                algorithms=["ES256"],
                audience=settings.APP_BUNDLE_ID,
                options={"verify_exp": True}
            )

            if payload.get("app_id") != settings.APP_BUNDLE_ID or \
               payload.get("device_id") != expected_device_id or \
               payload.get("challenge") != expected_challenge:
                raise ValueError("Invalid token payload")

            return payload

        except JWTError:
            continue
        except ValueError as ve:
            raise ve
    raise ValueError("Failed attestation validation")

def get_current_session(authorization: str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        if payload.get("type") != "attested_session":
            raise HTTPException(status_code=403, detail="Invalid session type")
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid or expired session token")
