import sqlite3
import json
import requests
import sys
from datetime import datetime

# ---- CONFIG ----
DB_PATH = "Automated-Smart-Home-Scheduler\events.db"
HA_URL = "http://localhost:8123"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI1NTEyODcxNjRjYjk0ZjVjYTkzN2MxYTMwNDI1NDUxNyIsImlhdCI6MTc0NDgzNTExNSwiZXhwIjoyMDYwMTk1MTE1fQ.j3wrP1rH60XfQpZbteE0utUINuPyC5oeLI6SAN8nhb4"  # Replace with actual token
ENTITY_ID = "input_text.schedule_data"

# ---- Get date argument (e.g., '2025-04-16') ----
if len(sys.argv) < 2:
    print("Usage: fetch_schedule.py YYYY-MM-DD")
    sys.exit(1)

target_date = sys.argv[1]

# ---- Connect to the database ----
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ---- Get Date_ID ----
cursor.execute("SELECT Date_ID FROM Date WHERE Date = ?", (target_date,))
row = cursor.fetchone()
if not row:
    schedule_data = []
else:
    date_id = row[0]
    # ---- Get schedule for that Date_ID ----
    cursor.execute("SELECT Time, Name FROM Schedule WHERE Date_ID = ?", (date_id,))
    schedule_data = [{"time": time, "name": name} for time, name in cursor.fetchall()]

conn.close()

# ---- Convert to JSON ----
json_data = json.dumps(schedule_data)

# ---- Send to Home Assistant ----
headers = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}

response = requests.post(
    f"{HA_URL}/api/states/{ENTITY_ID}",
    headers=headers,
    json={"state": json_data}
)

if response.status_code == 200:
    print("Schedule updated successfully.")
else:
    print(f"Error updating schedule: {response.status_code}")
    print(response.text)