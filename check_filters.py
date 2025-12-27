#!/usr/bin/env python3
"""現在のフィルタリング条件確認"""

import requests
import json

url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
events = response.json()

print(f"📊 今週の経済指標統計\n")
print(f"総イベント数: {len(events)}")

# Impact別の集計
impacts = {}
for e in events:
    impact = e.get('impact', 'Unknown')
    impacts[impact] = impacts.get(impact, 0) + 1

print("\n【重要度別】")
for impact, count in sorted(impacts.items()):
    print(f"  {impact}: {count}件")

# High impactのみ抽出
high_events = [e for e in events if e.get('impact') == 'High']

print(f"\n【High Impact指標】 {len(high_events)}件")

# 国別集計
countries = {}
for e in high_events:
    country = e.get('country')
    countries[country] = countries.get(country, 0) + 1

print("\n国別:")
for country, count in sorted(countries.items()):
    print(f"  {country}: {count}件")

print("\n\n【全High Impact指標リスト】")
print("=" * 80)
for e in sorted(high_events, key=lambda x: x.get('date')):
    print(f"{e['country']:4s} | {e['date'][:10]} | {e['title']}")
