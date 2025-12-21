# Discord Bot セットアップガイド

## 📋 必要な情報

1. **Discord Bot Token**
2. **Discord Channel ID**

---

## 🤖 Step 1: Discord Botの作成

### 1-1. Discord Developer Portalにアクセス

https://discord.com/developers/applications にアクセス

### 1-2. 新しいApplicationを作成

1. 「New Application」をクリック
2. 名前を入力（例: `経済指標Bot`）
3. 「Create」をクリック

### 1-3. Botを追加

1. 左メニューから「Bot」を選択
2. 「Add Bot」→「Yes, do it!」をクリック
3. Bot Tokenをコピー
   - 「Reset Token」→「Copy」

⚠️ **重要**: Tokenは他人に見せないでください！

### 1-4. Bot権限の設定

「Bot」ページで以下を設定:

**Privileged Gateway Intents:**
- ✅ MESSAGE CONTENT INTENT（メッセージ内容を読む権限）

**Bot Permissions:**
- ✅ View Channels（チャンネルを見る）
- ✅ Send Messages（メッセージを送る）
- ✅ Manage Messages（メッセージを管理 = 削除）
- ✅ Read Message History（メッセージ履歴を読む）

### 1-5. BotをサーバーにInvite

1. 左メニューから「OAuth2」→「URL Generator」を選択
2. **SCOPES** で `bot` にチェック
3. **BOT PERMISSIONS** で以下にチェック:
   - View Channels
   - Send Messages
   - Manage Messages
   - Read Message History
4. 生成されたURLをコピーしてブラウザで開く
5. サーバーを選択して「認証」

---

## 📍 Step 2: Channel IDの取得

### 2-1. Discordで開発者モードを有効化

1. Discord設定を開く
2. 「詳細設定」→「開発者モード」をON

### 2-2. チャンネルIDをコピー

1. 経済指標を送信したいチャンネルを右クリック
2. 「IDをコピー」をクリック

---

## 🔐 Step 3: 環境変数の設定

### ローカル環境

`.env`ファイルを編集:

```bash
DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
DISCORD_CHANNEL_ID=123456789012345678
```

### GitHub Actions

1. GitHubリポジトリの **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** で以下を追加:

| Name | Value |
|------|-------|
| `DISCORD_BOT_TOKEN` | BotのToken |
| `DISCORD_CHANNEL_ID` | チャンネルID |

---

## ✅ Step 4: テスト実行

```bash
./run_local.sh
```

以下が表示されれば成功:
```
✅ Botログイン成功: 経済指標Bot#1234
📍 送信先チャンネル: 経済指標
✅ 処理が正常に完了しました
```

---

## ⚙️ スケジュール設定

GitHub Actionsは以下のスケジュールで自動実行されます:

| 時刻 | 動作 |
|------|------|
| **毎週土曜 22:00 JST** | 来週のカレンダー送信 |
| **毎日 6:00 JST** | 実績データで更新 |

---

## 🔧 トラブルシューティング

### Bot Tokenエラー
→ TOKEN が正しいか確認、Resetした場合は新しいTokenを使用

### チャンネルが見つからない
→ Channel IDが正しいか確認、BotがサーバーにJoinしているか確認

### 権限エラー
→ Bot権限で「Manage Messages」が有効か確認

### メッセージが削除されない
→ `message_state.json` の内容を確認

---

## 📝 message_state.json の役割

週ごとのメッセージIDを保存:

```json
{
  "current_week": "2025-12-22",
  "message_id": "123456789"
}
```

- 同じ週 → 古いメッセージ削除
- 新しい週 → 古いメッセージ保持
