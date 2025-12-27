#!/usr/bin/env python3
"""Forex Factory APIの実績値フィールド確認"""

import requests
import json
from datetime import datetime, timedelta

url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers, timeout=15)
data = response.json()

print(f"取得件数: {len(data)}\n")

# 過去のイベント（発表済み）を探す
now = datetime.now()
past_events = []

for event in data:
    try:
        from dateutil import parser as date_parser
        event_time = date_parser.isoparse(event['date'])
        
        # 過去のイベントかつHigh impactのみ
        if event_time < now and event.get('impact') == 'High':
            past_events.append(event)
    except:
        continue

print(f"過去の重要指標: {len(past_events)}件\n")
print("=" * 80)

for i, event in enumerate(past_events[:5], 1):
    print(f"\n【過去イベント {i}】")
    print(f"タイトル: {event.get('title')}")
    print(f"国: {event.get('country')}")
    print(f"日時: {event.get('date')}")
    print(f"影響: {event.get('impact')}")
    print(f"予想: {event.get('forecast')}")
    print(f"前回: {event.get('previous')}")
    print(f"実績: {event.get('actual')}")  # ここが重要
    print("\n全フィールド:")
    print(json.dumps(event, indent=2, ensure_ascii=False))
    print("-" * 80)
