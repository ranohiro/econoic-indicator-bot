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


def get_current_week_range():
    """今週の日曜日から土曜日までの日付を取得"""
    today = datetime.datetime.now()
    
    # 今週の日曜日を算出（0=月曜, 6=日曜）
    days_since_sunday = (today.weekday() + 1) % 7
    
    # 今週の日曜日
    this_sunday = today - datetime.timedelta(days=days_since_sunday)
    this_saturday = this_sunday + datetime.timedelta(days=6)
    
    # 時刻を設定
    this_sunday = this_sunday.replace(hour=0, minute=0, second=0, microsecond=0)
    this_saturday = this_saturday.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    return this_sunday, this_saturday


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


async def send_calendar_message(channel, events, start_date, end_date, client):
    """カレンダーメッセージを送信し、必要に応じて古いメッセージを削除"""
    week_start = start_date.strftime('%Y-%m-%d')
    week_end = end_date.strftime('%Y-%m-%d')
    week_identifier = f"{week_start} 〜 {week_end}"
    
    # Botが送信した同じ週のメッセージを検索・削除
    print(f"🔍 過去のメッセージを検索中（対象週: {week_identifier}）...")
    deleted_count = 0
    
    try:
        async for message in channel.history(limit=100):
            # 自分（Bot）が送信したメッセージのみ対象
            if message.author.id == client.user.id:
                # メッセージ内容に同じ週の範囲が含まれているか確認
                if week_identifier in message.content:
                    try:
                        await message.delete()
                        deleted_count += 1
                        print(f"🗑️  古いメッセージを削除: ID {message.id}")
                    except discord.NotFound:
                        print(f"⚠️  メッセージが既に削除されています: ID {message.id}")
                    except Exception as e:
                        print(f"❌ メッセージ削除エラー: {e}")
    except Exception as e:
        print(f"❌ メッセージ検索エラー: {e}")
    
    if deleted_count > 0:
        print(f"✅ {deleted_count}件の古いメッセージを削除しました")
    else:
        print(f"📌 削除対象のメッセージはありませんでした（新規週または初回実行）")
    
    # 新しいメッセージを送信
    messages = create_discord_message(events, start_date, end_date)
    
    sent_message = None
    for i, msg_content in enumerate(messages, 1):
        sent_message = await channel.send(msg_content)
        print(f"📤 メッセージ {i}/{len(messages)} を送信しました")
    
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
            
            # 今週の日付範囲を取得
            start_date, end_date = get_current_week_range()
            print(f"📅 対象期間: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")
            
            # 日付範囲でフィルタリング
            week_events = filter_by_date_range(all_events, start_date, end_date)
            
            # 重要度が高い指標のみ抽出
            high_impact_events = filter_high_impact_events(week_events)
            
            # メッセージ送信（古いメッセージ管理含む）
            await send_calendar_message(channel, high_impact_events, start_date, end_date, client)
            
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
