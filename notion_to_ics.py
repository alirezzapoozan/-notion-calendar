import os
import json
import requests
from datetime import datetime, timezone
from icalendar import Calendar, Event, vText
import uuid

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = "2c7e1e4a-8a90-81d8-bcdd-000bad6c15b6"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def fetch_tasks():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {
        "filter": {
            "and": [
                {
                    "property": "انجام شده",
                    "checkbox": {"equals": False}
                },
                {
                    "property": "تاریخ",
                    "date": {"is_not_empty": True}
                }
            ]
        }
    }
    
    all_results = []
    has_more = True
    start_cursor = None

    while has_more:
        if start_cursor:
            payload["start_cursor"] = start_cursor
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        all_results.extend(data.get("results", []))
        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor")

    return all_results

def build_ics(tasks):
    cal = Calendar()
    cal.add("prodid", "-//Notion Tasks//notion-to-ics//FA")
    cal.add("version", "2.0")
    cal.add("calscale", "GREGORIAN")
    cal.add("method", "PUBLISH")
    cal.add("x-wr-calname", vText("کارها - Notion"))
    cal.add("x-wr-timezone", vText("Asia/Tehran"))
    cal.add("refresh-interval;value=duration", "PT15M")
    cal.add("x-published-ttl", "PT15M")

    type_emojis = {
        "کسب و کار": "💼",
        "University": "🎓",
        "شخصی": "👤",
        "Python": "🐍",
    }

    for page in tasks:
        props = page["properties"]

        # Title
        title_arr = props.get("کار", {}).get("title", [])
        title = "".join(t.get("plain_text", "") for t in title_arr) or "بدون عنوان"

        # Date
        date_prop = props.get("تاریخ", {}).get("date")
        if not date_prop or not date_prop.get("start"):
            continue
        
        start_raw = date_prop["start"]
        end_raw = date_prop.get("end")

        # Type / category
        task_type = props.get("نوع", {}).get("select", {})
        type_name = task_type.get("name", "") if task_type else ""
        emoji = type_emojis.get(type_name, "📌")

        # Description
        desc_arr = props.get("توضیحات", {}).get("rich_text", [])
        description = "".join(t.get("plain_text", "") for t in desc_arr)
        notion_url = page.get("url", "")
        if notion_url:
            description += f"\n\n🔗 {notion_url}"

        event = Event()
        event.add("uid", vText(str(uuid.UUID(page["id"]))))
        event.add("summary", vText(f"{emoji} {title}"))

        # Parse date or datetime
        def parse_dt(raw):
            if "T" in raw:
                dt = datetime.fromisoformat(raw)
                if dt.tzinfo is None:
                    from zoneinfo import ZoneInfo
                    dt = dt.replace(tzinfo=ZoneInfo("Asia/Tehran"))
                return dt
            else:
                from datetime import date as dt_date
                return datetime.strptime(raw, "%Y-%m-%d").date()

        start_dt = parse_dt(start_raw)
        event.add("dtstart", start_dt)

        if end_raw:
            end_dt = parse_dt(end_raw)
            event.add("dtend", end_dt)

        event.add("description", vText(description))
        if type_name:
            event.add("categories", vText(type_name))

        event.add("dtstamp", datetime.now(timezone.utc))
        cal.add_component(event)

    return cal.to_ical()

def main():
    print("📥 Fetching tasks from Notion...")
    tasks = fetch_tasks()
    print(f"✅ Found {len(tasks)} tasks with dates")

    ics_data = build_ics(tasks)

    os.makedirs("docs", exist_ok=True)
    with open("docs/tasks.ics", "wb") as f:
        f.write(ics_data)

    print("📅 ICS file saved to docs/tasks.ics")

if __name__ == "__main__":
    main()
