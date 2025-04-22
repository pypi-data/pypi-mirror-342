from prettytable import PrettyTable
import requests
from pathlib import Path
import json
from datetime import datetime

TOKEN_FILE = Path("auth_token.json")
TASK_ID_FILE = Path("task_id.txt")
API_URL = "http://148.66.158.143:8000/api/v1/employee/report"

def get_token():
    if TOKEN_FILE.exists():
        try:
            data = json.loads(TOKEN_FILE.read_text())
            return data.get("access_token")
        except Exception:
            return None
    return None

def get_next_task_id():
    """Simple incremental ID for task tracking"""
    try:
        if TASK_ID_FILE.exists():
            task_id = int(TASK_ID_FILE.read_text()) + 1
        else:
            task_id = 1
        TASK_ID_FILE.write_text(str(task_id))
        return str(task_id)
    except Exception:
        return "1"

def submit_report(report_summary: str, project_title: str, status: str):
    token = get_token()
    if not token:
        return "⚠️ No token found. Please login first."

    payload = {
        "report_summary": report_summary,
        "project_title": project_title,
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "status": status,
        "task_id": get_next_task_id()
    }

    headers = {
        "Authorization": f"{token}"
    }
    
    print(f"Submitting report with payload: {payload}")

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return "📝 Report submitted successfully."
    except requests.HTTPError as e:
        return f"❌ Report submission failed: {e}\n{response.text}"
    except Exception as e:
        return f"❌ Error: {e}"

def list_reports():
    
    token = get_token()
    if not token:
        return "⚠️ No token found. Please login first."
    
    headers = {
        "Authorization": f"{token}"
    }
    
    # Make the GET request to the API
    response = requests.get(API_URL, headers=headers)
    if response.status_code != 200:
        return f"❌ Failed to fetch reports. Status Code: {response.status_code}"

    # Parse the JSON response
    reports = response.json()

    if not reports:
        return "📭 No reports found."

    # Initialize PrettyTable
    table = PrettyTable()
    table.field_names = ["Employee ID", "Report ID", "Project Title", "Date", "Status", "Summary"]

    # Add rows to the table
    for r in reports["data"]["employee_report"]:
        table.add_row([
            r["employee_id"],
            r["employee_report_id"],
            r["project_title"],
            r["report_date"],
            r["status"],
            r["report_summary"].split("\n")
        ])

    return table.get_string()
    