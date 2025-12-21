#!/usr/bin/env python3
"""
経済指標Discord自動通知ツール (Discord Bot版)

Forex Factory Economic Calendar JSON から重要経済指標を取得し、
Discord Botで特定チャンネルに送信。週ごとにメッセージを管理。
"""

import os
import sys
import json
import datetime
import requests
import discord
from dotenv import load_dotenv
from dateutil import parser

# .envファイルから環境変数を読み込み
load_dotenv()

# 定数定義
DISCORD_CHAR_LIMIT = 2000
MESSAGE_STATE_FILE = "message_state.json"

# 通貨/国コードを旗に変換
COUNTRY_FLAGS = {
    'USD': '🇺🇸', 'JPY': '🇯🇵', 'EUR': '🇪🇺', 'GBP': '🇬🇧',
    'AUD': '🇦🇺', 'CAD': '🇨🇦', 'CHF': '🇨🇭', 'NZD': '🇳🇿',
    'CNY': '🇨🇳', 'KRW': '🇰🇷', 'SGD': '🇸🇬',
}


def fetch_forex_factory_calendar():
    """Forex Factoryの公開JSONから今週の経済指標を取得"""
    url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    print(f"📡 Forex Factory APIにリクエスト中...")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        events = response.json()
        print(f"✅ {len(events)}件の経済指標を取得")
        return events
    except Exception as e:
        print(f"❌ データ取得エラー: {e}")
        raise


def filter_high_impact_events(events):
    """重要度が 'High' の指標のみをフィルタリング"""
    filtered = [e for e in events if e.get('impact') == 'High']
    print(f"🔍 高インパクト指標: {len(filtered)}件")
    return filtered


def get_next_week_range():
    """翌週の日曜日から土曜日までの日付を取得"""
    today = datetime.datetime.now()
    days_until_sunday = (6 - today.weekday() + 7) % 7
    if days_until_sunday == 0:
        days_until_sunday = 7  # 本番用: 翌週（テスト時は0）
    
    start_date = today + datetime.timedelta(days=days_until_sunday)
    end_date = start_date + datetime.timedelta(days=6)
    
    start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    return start_date, end_date


def filter_by_date_range(events, start_date, end_date):
    """指定された日付範囲内のイベントのみをフィルタリング"""
    filtered = []
    
    for e in events:
        date_str = e.get('date', '')
        try:
            event_datetime = parser.isoparse(date_str)
            event_date_only = event_datetime.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
            start_date_only = start_date.replace(tzinfo=None)
            end_date_only = end_date.replace(hour=23, minute=59, second=59, microsecond=999999, tzinfo=None)
            
            if start_date_only <= event_date_only <= end_date_only:
                filtered.append(e)
        except:
            continue
    
    print(f"📅 対象期間内の指標: {len(filtered)}件")
    return filtered


def create_discord_message(events, start_date, end_date):
    """Discord用のメッセージを生成"""
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    
    if not events:
        return [f"📅 **【経済指標カレンダー】 {start_str} 〜 {end_str}**\n\n✅ 重要経済指標（High）の予定がありません。"]
    
    messages = []
    header = f"📢 **【経済指標カレンダー】 {start_str} 〜 {end_str}**\n"
    header += "------------------------------------------\n"
    current_message = header
    
    sorted_events = sorted(events, key=lambda x: x.get('date', ''))
    
    for e in sorted_events:
        date_str = e.get('date', '未定')
        
        try:
            event_datetime = parser.isoparse(date_str)
            jst_datetime = event_datetime + datetime.timedelta(hours=14)
            time_display = jst_datetime.strftime('%m/%d %H:%M')
        except:
            time_display = date_str
        
        currency = e.get('country', 'XX')
        flag = COUNTRY_FLAGS.get(currency, '🏳️')
        event_name = e.get('title', '不明な指標')
        forecast = e.get('forecast', '-')
        previous = e.get('previous', '-')
        actual = e.get('actual', '')
        
        # 実績データがあれば表示
        if actual:
            line = f"🕒 `{time_display}` {flag} **{event_name}**\n"
            line += f"   ┗ 結果: `{actual}` / 予: `{forecast}` / 前: `{previous}`\n\n"
        else:
            line = f"🕒 `{time_display}` {flag} **{event_name}**\n"
            line += f"   ┗ 予: `{forecast}` / 前: `{previous}`\n\n"
        
        if len(current_message) + len(line) > 1900:
            messages.append(current_message.strip())
            current_message = line
        else:
            current_message += line
    
    if current_message.strip():
        messages.append(current_message.strip())
    
    return messages


def load_message_state():
    """メッセージ状態をファイルから読み込み"""
    if os.path.exists(MESSAGE_STATE_FILE):
        try:
            with open(MESSAGE_STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_message_state(week_start, message_id):
    """メッセージ状態をファイルに保存"""
    state = {
        "current_week": week_start,
        "message_id": str(message_id)
    }
    with open(MESSAGE_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)
    print(f"💾 メッセージ状態を保存: {week_start}")


async def send_calendar_message(channel, events, start_date, end_date):
    """カレンダーメッセージを送信し、必要に応じて古いメッセージを削除"""
    week_start = start_date.strftime('%Y-%m-%d')
    state = load_message_state()
    
    # 前回のメッセージ確認
    should_delete_old = False
    if state.get('current_week') and state.get('message_id'):
        # 同じ週なら古いメッセージを削除
        if state['current_week'] == week_start:
            should_delete_old = True
            old_message_id = int(state['message_id'])
            print(f"🗑️  同じ週のため、古いメッセージ削除: {old_message_id}")
        else:
            print(f"📌 新しい週のため、前週メッセージは保持")
    
    # 古いメッセージを削除
    if should_delete_old:
        try:
            old_message = await channel.fetch_message(old_message_id)
            await old_message.delete()
            print(f"✅ 古いメッセージを削除")
        except discord.NotFound:
            print(f"⚠️  古いメッセージが見つかりません")
        except Exception as e:
            print(f"❌ メッセージ削除エラー: {e}")
    
    # 新しいメッセージを送信
    messages = create_discord_message(events, start_date, end_date)
    
    sent_message = None
    for i, msg_content in enumerate(messages, 1):
        sent_message = await channel.send(msg_content)
        if i == 1:  # 最初のメッセージIDのみ保存
            save_message_state(week_start, sent_message.id)
    
    return sent_message


async def main():
    """メイン処理"""
    print("=" * 60)
    print("経済指標Discord自動通知ツール (Discord Bot版)")
    print("=" * 60)
    
    # 環境変数から認証情報を取得
    bot_token = os.getenv("DISCORD_BOT_TOKEN")
    channel_id = os.getenv("DISCORD_CHANNEL_ID")
    
    if not bot_token:
        print("❌ エラー: DISCORD_BOT_TOKEN が設定されていません")
        sys.exit(1)
    
    if not channel_id:
        print("❌ エラー: DISCORD_CHANNEL_ID が設定されていません")
        sys.exit(1)
    
    try:
        channel_id = int(channel_id)
    except:
        print("❌ エラー: DISCORD_CHANNEL_ID が数値ではありません")
        sys.exit(1)
    
    # Discord Bot クライアント作成
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f'✅ Botログイン成功: {client.user}')
        
        try:
            # チャンネル取得
            channel = client.get_channel(channel_id)
            if not channel:
                print(f"❌ チャンネルが見つかりません: {channel_id}")
                await client.close()
                return
            
            print(f"📍 送信先チャンネル: {channel.name}")
            
            # Forex Factoryからデータ取得
            all_events = fetch_forex_factory_calendar()
            
            # 翌週の日付範囲を取得
            start_date, end_date = get_next_week_range()
            print(f"📅 対象期間: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")
            
            # 日付範囲でフィルタリング
            week_events = filter_by_date_range(all_events, start_date, end_date)
            
            # 重要度が高い指標のみ抽出
            high_impact_events = filter_high_impact_events(week_events)
            
            # メッセージ送信（古いメッセージ管理含む）
            await send_calendar_message(channel, high_impact_events, start_date, end_date)
            
            print("=" * 60)
            print("✅ 処理が正常に完了しました")
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ エラー: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await client.close()
    
    # Bot起動
    await client.start(bot_token)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
