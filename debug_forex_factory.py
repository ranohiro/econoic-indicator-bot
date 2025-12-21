#!/usr/bin/env python3
"""デバッグスクリプト: Forex Factoryのデータ構造を確認"""

import requests
import json

url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

response = requests.get(url, headers=headers, timeout=15)
data = response.json()

print(f"取得件数: {len(data)}")
print("\n最初の5件のデータ構造:")
print("=" * 80)

for i, event in enumerate(data[:5], 1):
    print(f"\n【イベント {i}】")
    print(json.dumps(event, indent=2, ensure_ascii=False))
    print("-" * 80)

# 重要度Highの最初の3件
print("\n\n重要度 'High' のイベント:")
print("=" * 80)
high_events = [e for e in data if e.get('impact') == 'High']
for i, event in enumerate(high_events[:3], 1):
    print(f"\n【High Impact {i}】")
    print(json.dumps(event, indent=2, ensure_ascii=False))
    print("-" * 80)
