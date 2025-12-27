# 経済指標Discord Bot

Forex Factoryから経済指標を自動収集し、週1回Discordに通知するBotです。
投資判断に重要な指標（米国・日本・中国）を厳選して配信します。

## 📊 機能

- **週次配信**: 毎週日曜 18:00 (JST) に今週のカレンダーを通知
- **厳選フィルタリング**:
  - 対象国: 🇺🇸 米国、🇯🇵 日本、🇨🇳 中国
  - **High Impact**: すべて
  - **Medium Impact**: 重要なキーワード（CPI, 雇用統計, 金利政策など）
- **自動更新**: 同じ週に再実行された場合、古いメッセージを自動削除して最新情報を送信

## 🚀 セットアップ

### 1. 準備
- Discord Bot Tokenの取得
- 送信先チャンネルIDの取得

### 2. 環境変数 (.env)
```bash
DISCORD_BOT_TOKEN=your_token_here
DISCORD_CHANNEL_ID=your_channel_id_here
```

### 3. ローカル実行
```bash
# インストール
pip install -r requirements.txt

# 実行
python src/economic_calendar.py
```

## ⚙️ 自動運用 (GitHub Actions)

リポジトリの **Settings > Secrets** に以下を設定することで、毎週日曜18:00に自動実行。

| Name | Value |
|------|-------|
| `DISCORD_BOT_TOKEN` | Botトークン |
| `DISCORD_CHANNEL_ID` | チャンネルID |

## 📝 免責事項
本ツールは情報提供を目的としています。投資判断は自己責任で行ってください。
