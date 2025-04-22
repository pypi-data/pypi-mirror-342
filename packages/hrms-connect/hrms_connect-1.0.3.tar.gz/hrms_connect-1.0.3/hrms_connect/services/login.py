import requests
import json
from pathlib import Path
from datetime import datetime, timezone
import jwt  # install with: pip install PyJWT

API_BASE = "http://148.66.158.143:8000/api/v1/user"
TOKEN_FILE = Path("auth_token.json")


def login(email: str, password: str) -> str:
    url = f"{API_BASE}/login"
    payload = {
        "user_email": email,
        "user_password": password
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()["data"]

        access_token = data["access_token"]
        refresh_token = data["refresh_token"]
        user_id = data["user"]["user_id"]

        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        expiry = decoded_token.get("exp")

        auth_data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user_id,
            "expiry": expiry
        }

        TOKEN_FILE.write_text(json.dumps(auth_data, indent=2))
        return "✅ Login successful! Token saved."
    except requests.HTTPError as e:
        return f"❌ Login failed: {e}\n{response.text}"
    except Exception as e:
        return f"❌ Unexpected error: {e}"


def get_token_data():
    if TOKEN_FILE.exists():
        return json.loads(TOKEN_FILE.read_text())
    return None


def is_token_expired() -> bool:
    data = get_token_data()
    if not data:
        return True
    exp = data.get("expiry")
    if not exp:
        return True
    current_time = datetime.now(timezone.utc).timestamp()
    return current_time >= exp


def get_valid_access_token() -> str | None:
    if is_token_expired():
        return None
    return get_token_data().get("access_token")


def clear_token():
    TOKEN_FILE.unlink(missing_ok=True)
