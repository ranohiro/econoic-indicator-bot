#!/usr/bin/env python3
"""
テストスクリプト: economic_calendar.pyの機能を検証
APIキーがなくてもロジックをテストできるようにモック機能を追加
"""

import sys
import os
from datetime import datetime
import pytz

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from economic_calendar import (
    get_next_week_dates,
    filter_high_impact_events,
    format_value,
    convert_utc_to_jst,
    create_discord_message
)


def test_get_next_week_dates():
    """翌週の日付範囲取得のテスト"""
    print("=" * 60)
    print("テスト1: 翌週の日付範囲取得")
    print("=" * 60)
    
    start_date, end_date = get_next_week_dates()
    print(f"✅ 開始日: {start_date}")
    print(f"✅ 終了日: {end_date}")
    
    # 日曜日から土曜日までの7日間であることを確認
    from datetime import datetime, timedelta
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    diff = (end - start).days
    
    assert diff == 6, f"期間が7日間ではありません: {diff + 1}日間"
    assert start.weekday() == 6, f"開始日が日曜日ではありません: {start.strftime('%A')}"
    
    print("✅ テスト1合格: 正しい日付範囲が取得されました\n")


def test_filter_high_impact_events():
    """高インパクト指標のフィルタリングテスト"""
    print("=" * 60)
    print("テスト2: 高インパクト指標のフィルタリング")
    print("=" * 60)
    
    # サンプルデータ
    mock_events = [
        {"event": "GDP", "impact": "high", "country": "US"},
        {"event": "CPI", "impact": "medium", "country": "JP"},
        {"event": "Retail Sales", "impact": "high", "country": "EU"},
        {"event": "PMI", "impact": "low", "country": "GB"},
    ]
    
    filtered = filter_high_impact_events(mock_events)
    
    print(f"✅ 元データ: {len(mock_events)}件")
    print(f"✅ フィルタ後: {len(filtered)}件")
    
    assert len(filtered) == 2, f"期待値2件、実際は{len(filtered)}件"
    assert all(e["impact"] == "high" for e in filtered), "highでない指標が含まれています"
    
    print("✅ テスト2合格: 正しくフィルタリングされました\n")


def test_format_value():
    """数値フォーマットのテスト"""
    print("=" * 60)
    print("テスト3: 数値フォーマット")
    print("=" * 60)
    
    assert format_value(0.5) == "0.5", "数値のフォーマットが正しくありません"
    assert format_value(None) == "-", "Noneの処理が正しくありません"
    assert format_value("") == "-", "空文字列の処理が正しくありません"
    
    print("✅ 数値: 0.5 → '0.5'")
    print("✅ None → '-'")
    print("✅ 空文字列 → '-'")
    print("✅ テスト3合格: 正しくフォーマットされました\n")


def test_convert_utc_to_jst():
    """UTC→JST変換のテスト"""
    print("=" * 60)
    print("テスト4: UTC→JST時刻変換")
    print("=" * 60)
    
    # 2025-01-15 13:30:00 UTC
    utc_time = "2025-01-15T13:30:00Z"
    jst_time = convert_utc_to_jst(utc_time)
    
    print(f"✅ UTC: {utc_time}")
    print(f"✅ JST: {jst_time}")
    
    # JSTはUTC+9なので、13:30 → 22:30になるはず
    assert "22:30" in jst_time, f"時刻変換が正しくありません: {jst_time}"
    
    print("✅ テスト4合格: 正しく変換されました\n")


def test_create_discord_message():
    """Discordメッセージ生成のテスト"""
    print("=" * 60)
    print("テスト5: Discordメッセージ生成")
    print("=" * 60)
    
    # サンプルデータ
    mock_events = [
        {
            "country": "US",
            "event": "GDP Growth Rate",
            "time": "2025-01-15T13:30:00Z",
            "previous": 0.3,
            "estimate": 0.5,
            "impact": "high"
        },
        {
            "country": "JP",
            "event": "Core CPI",
            "time": "2025-01-16T23:50:00Z",
            "previous": 2.5,
            "estimate": 2.6,
            "impact": "high"
        }
    ]
    
    messages = create_discord_message(mock_events, "2025-01-12", "2025-01-18")
    
    print(f"✅ 生成されたメッセージ数: {len(messages)}")
    print(f"✅ メッセージ1の文字数: {len(messages[0])}")
    
    # メッセージ内容の確認
    assert len(messages) >= 1, "メッセージが生成されていません"
    assert "📊" in messages[0], "ヘッダーが含まれていません"
    assert "🇺🇸" in messages[0], "国旗が含まれていません"
    assert "GDP Growth Rate" in messages[0], "指標名が含まれていません"
    
    print("\n--- 生成されたメッセージ ---")
    for i, msg in enumerate(messages, 1):
        print(f"\n[メッセージ {i}]")
        print(msg)
        print(f"\n文字数: {len(msg)}/2000")
    
    print("\n✅ テスト5合格: 正しくメッセージが生成されました\n")


def test_empty_events():
    """指標が0件の場合のテスト"""
    print("=" * 60)
    print("テスト6: 指標0件の処理")
    print("=" * 60)
    
    messages = create_discord_message([], "2025-01-12", "2025-01-18")
    
    assert len(messages) == 1, "メッセージが1件ではありません"
    assert "今週は重要経済指標の予定がありません" in messages[0], "空メッセージが正しくありません"
    
    print("✅ メッセージ: " + messages[0])
    print("✅ テスト6合格: 正しく処理されました\n")


def run_all_tests():
    """すべてのテストを実行"""
    print("\n" + "=" * 60)
    print("経済指標Discord通知ツール - 機能テスト")
    print("=" * 60 + "\n")
    
    try:
        test_get_next_week_dates()
        test_filter_high_impact_events()
        test_format_value()
        test_convert_utc_to_jst()
        test_create_discord_message()
        test_empty_events()
        
        print("=" * 60)
        print("✅ すべてのテストが合格しました！")
        print("=" * 60)
        print("\n次のステップ:")
        print("1. Finnhub APIキーを取得")
        print("2. Discord Webhook URLを取得")
        print("3. 環境変数を設定して実際のAPIで動作確認")
        print("4. GitHubにプッシュしてGitHub Actionsをセットアップ")
        print("=" * 60)
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ テスト失敗: {e}")
        return False
    except Exception as e:
        print(f"\n❌ エラー発生: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
