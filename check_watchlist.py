#!/usr/bin/env python3
"""ユーザーのウォッチリストに該当する指標を確認"""

import requests
import json

url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
headers = {"User-Agent": "Mozilla/5.0"}

# ユーザーが求める指標のキーワード
KEYWORDS = [
    # 米国
    'CPI', 'PCE', 'PPI',
    'Non-Farm', 'Unemployment', 'JOLTS',
    'ISM Manufacturing', 'ISM Services', 'PMI',
    'Retail Sales', 'Consumer Sentiment',
    'Federal Funds', 'FOMC',
    # 日本
    'Tokyo CPI', 'Core CPI',
    'Tankan',
    'BOJ', 'Policy Rate', 'Monetary Policy',
    'Trade Balance',
    # 中国
    'Manufacturing PMI'
]

TARGET_COUNTRIES = ['USD', 'JPY', 'CNY']

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    events = response.json()
except Exception as e:
    print(f"Error: {e}")
    exit(1)

print(f"📊 Forex Factory 今週のデータ分析\n")
print(f"総イベント数: {len(events)}\n")

# 重要3カ国のイベント
target_events = [e for e in events if e.get('country') in TARGET_COUNTRIES]
print(f"【対象国（USD, JPY, CNY）】 {len(target_events)}件\n")

# Impact別
for country in TARGET_COUNTRIES:
    country_events = [e for e in target_events if e.get('country') == country]
    high = len([e for e in country_events if e.get('impact') == 'High'])
    medium = len([e for e in country_events if e.get('impact') == 'Medium'])
    print(f"{country}: {len(country_events)}件 (High: {high}, Medium: {medium})")

# キーワードマッチ
print(f"\n【ウォッチリストに該当する指標】")
print("=" * 80)

matched = []
for event in target_events:
    title = event.get('title', '')
    for keyword in KEYWORDS:
        if keyword.lower() in title.lower():
            matched.append(event)
            break

# 重複削除
matched = list({e['title']: e for e in matched}.values())

print(f"該当件数: {len(matched)}件\n")

for e in sorted(matched, key=lambda x: (x.get('country'), x.get('date'))):
    impact_emoji = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}.get(e.get('impact'), '⚪')
    print(f"{impact_emoji} {e['country']:4s} | {e['date'][:10]} | {e['title']}")

# High/Mediumの全指標も表示
print(f"\n\n【参考：対象3カ国のHigh/Medium全指標】")
print("=" * 80)
high_medium = [e for e in target_events if e.get('impact') in ['High', 'Medium']]
print(f"件数: {len(high_medium)}件\n")

for e in sorted(high_medium, key=lambda x: (x.get('country'), x.get('date'))):
    impact_emoji = {'High': '🔴', 'Medium': '🟡'}.get(e.get('impact'), '⚪')
    print(f"{impact_emoji} {e['country']:4s} | {e['date'][:10]} | {e['title']}")
