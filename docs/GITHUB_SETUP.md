# GitHub リポジトリ作成 & プッシュガイド

## 📝 準備完了

✅ Git 初期化完了  
✅ ファイルステージング完了  
✅ .env ファイルは除外設定済み

---

## 🚀 Step 1: GitHubでリポジトリ作成

### 1-1. GitHub にアクセス

https://github.com にログイン

### 1-2. 新しいリポジトリ作成

1. 右上の **「+」** → **「New repository」** をクリック

2. **リポジトリ設定:**
   - **Repository name**: `economic-calendar-bot` （またはお好きな名前）
   - **Description**: `経済指標Discord自動通知Bot`
   - **Public** または **Private**: お好みで選択
   - ❌ **Initialize this repository with:** すべてチェックなし
     - README は追加しない（既にあるため）
     - .gitignore は追加しない
     - License も追加しない

3. **「Create repository」** をクリック

---

## 💻 Step 2: ローカルからプッシュ

### 2-1. GitHub表示されるコマンドをコピー

「…or push an existing repository from the command line」セクションのコマンドが表示されます。

例:
```bash
git remote add origin https://github.com/YOUR_USERNAME/economic-calendar-bot.git
git branch -M main
git push -u origin main
```

### 2-2. コミット

以下のコマンドを実行:

```bash
# 初回コミット
git commit -m "feat: Discord Bot経済指標通知システム完成"

# リモートリポジトリを追加（GitHubからコピーしたURL）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# ブランチ名を main に変更
git branch -M main

# プッシュ
git push -u origin main
```

⚠️ **認証が必要な場合:**
- Personal Access Token（PAT）が必要
- または GitHub CLI (`gh auth login`) を使用

---

## 🔐 Step 3: GitHub Secretsの設定

### 3-1. リポジトリの Settings に移動

1. GitHubのリポジトリページ
2. **Settings** タブをクリック

### 3-2. Secretsを追加

1. 左メニュー: **Secrets and variables** → **Actions**
2. **New repository secret** をクリック
3. 以下の2つを追加:

#### Secret 1: Discord Bot Token

- **Name**: `DISCORD_BOT_TOKEN`
- **Secret**: `.env`ファイルの `DISCORD_BOT_TOKEN` の値
- **Add secret** をクリック

#### Secret 2: Discord Channel ID

- **Name**: `DISCORD_CHANNEL_ID`
- **Secret**: `.env`ファイルの `DISCORD_CHANNEL_ID` の値
- **Add secret** をクリック

---

## ✅ Step 4: GitHub Actionsをテスト

### 4-1. 手動実行

1. リポジトリの **Actions** タブを開く
2. **Economic Calendar Notification** を選択
3. **Run workflow** → **Run workflow** をクリック
4. 実行状態を確認

### 4-2. Discordで確認

指定したチャンネルにメッセージが届いていればOK！

---

## 📅 自動実行スケジュール

以下のスケジュールで自動実行されます:

| 時刻 | 動作 |
|------|------|
| **毎週土曜 22:00 JST** | 来週のカレンダー送信 |
| **毎日 6:00 JST** | 実績データで更新 |

---

## 🔧 トラブルシューティング

### `git push` でエラー

**認証エラーの場合:**
```bash
# Personal Access Token を使用
# Username: あなたのGitHubユーザー名
# Password: Personal Access Token（PAT）
```

**PATの作成方法:**
1. GitHub Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token
4. `repo` にチェック → Generate

### GitHub Actions が動かない

1. Secretsが正しく設定されているか確認
2. `.github/workflows/economic_calendar.yml` が正しくプッシュされているか確認

---

## 🎉 完了！

これで経済指標Discord Bot が完全に稼働します！

毎週土曜の夜と毎朝、自動で経済指標が更新されます。
