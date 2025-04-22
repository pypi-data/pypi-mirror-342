import requests
from pathlib import Path
import json

TOKEN_FILE = Path("auth_token.json")
API_BASE = "http://148.66.158.143:8000/api/v1/user"

def logout():
    if not TOKEN_FILE.exists():
        return "⚠️ No token found. Please login first."

    try:
        data = json.loads(TOKEN_FILE.read_text())
        token = data.get("access_token")

        if not token:
            return "⚠️ Access token missing in token file."

        url = f"{API_BASE}/logout"
        headers = {
            "Authorization": f"{token}"
        }

        response = requests.post(url, headers=headers)
        response.raise_for_status()

        TOKEN_FILE.unlink(missing_ok=True)
        return "👋 Logged out successfully."

    except requests.HTTPError as e:
        return f"❌ Logout failed: {e}\n{response.text}"
    except Exception as e:
        return f"❌ Unexpected error: {e}"
