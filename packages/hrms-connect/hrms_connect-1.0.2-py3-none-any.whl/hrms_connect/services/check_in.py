import requests
from datetime import datetime
from pathlib import Path
import json

TOKEN_FILE = Path("auth_token.json")
API_BASE = "http://148.66.158.143:8000/api/v1/employee/log"
CHECK_IN_STATUS = "http://148.66.158.143:8000/api/v1/employee/attendance/status"


def check_in():
    # Read token from file
    if not TOKEN_FILE.exists():
        return "⚠️ No token found. Please login first."

    try:
        data = json.loads(TOKEN_FILE.read_text())
        token = data.get("access_token")

        if not token:
            return "⚠️ Access token missing in token file."

        # Get current datetime for check-in
        check_in_time = datetime.now().strftime("%H:%M:%S")
        check_in_date = datetime.now().strftime("%Y-%m-%d")

        # Prepare the payload
        payload = {
            "check_in": check_in_time,
            "attendance_date": check_in_date,
        }

        # Prepare the headers
        headers = {"Authorization": f"{token}"}
        
        print(f"Payload: {payload}")
        print(f"Headers: {headers}")

        # Make the POST request
        response = requests.post(API_BASE, json=payload, headers=headers)
        response.raise_for_status()

        return "✅ Successfully checked in."

    except requests.HTTPError as e:
        return f"❌ Check-in failed: {e}\n{response.text}"
    except Exception as e:
        return f"❌ Unexpected error: {e}"

def check_existing_check_in():
    # Read token from file
    if not TOKEN_FILE.exists():
        return "⚠️ No token found. Please login first."
    
    try:
        data = json.loads(TOKEN_FILE.read_text())
        token = data.get("access_token")

        if not token:
            return "⚠️ Access token missing in token file."
        
        headers = {"Authorization": f"{token}"}
        response = requests.get(CHECK_IN_STATUS, headers=headers)
        response.raise_for_status()
        
        check_in_data = response.json().get("data", {})
        print(f"Check-in data: {check_in_data}")
        if not check_in_data:
            return "⚠️ No check-in data found."
        
        if check_in_data.get("status") == "True":
            return "✅ You are already checked in."
        
        return None
    
    except requests.HTTPError as e:
        return f"❌ Failed to get check-in status: {e}\n{response.text}"
    except Exception as e:
        return f"❌ Unexpected error: {e}"