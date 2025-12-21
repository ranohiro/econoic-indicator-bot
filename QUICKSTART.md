# クイックスタートガイド

このガイドに従って、経済指標Discord自動通知ツールをセットアップしてください。

## 📋 前提条件

- Python 3.9以上がインストールされていること
- GitHubアカウント（GitHub Actions用）

## 🚀 ステップ1: ローカル環境で動作確認

### 1-1. APIキーとWebhook URLの取得

#### Finnhub APIキー
1. https://finnhub.io/ にアクセス
2. 無料アカウントを作成
3. ダッシュボードからAPIキーをコピー

#### Discord Webhook URL
1. Discordで通知先チャンネルを開く
2. チャンネル設定 → 連携サービス → ウェブフック
3. 「新しいウェブフック」を作成
4. Webhook URLをコピー

### 1-2. .envファイルの作成

```bash
cd /Users/hiranotakahiro/Projects/株価通知アプリ

# テンプレートをコピー
cp .env.example .env

# エディタで開いて実際の値を入力
# FINNHUB_API_KEY=取得したAPIキー
# DISCORD_WEBHOOK_URL=取得したWebhook URL
```

### 1-3. 実行

```bash
# 自動セットアップ＆実行
./run_local.sh
```

これで翌週の経済指標がDiscordに投稿されます！

## 🔄 ステップ2: GitHubで自動化

### 2-1. GitHubリポジトリの作成

```bash
# Gitリポジトリを初期化
git init
git add .
git commit -m "Initial commit: Economic Calendar Notification Tool"

# GitHubにプッシュ
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2-2. GitHub Secretsの設定

1. GitHubリポジトリのページで **Settings** タブを開く
2. 左メニューから **Secrets and variables** → **Actions** を選択
3. **New repository secret** をクリック
4. 以下の2つを追加:

**シークレット1:**
- Name: `FINNHUB_API_KEY`
- Secret: Finnhubから取得したAPIキー

**シークレット2:**
- Name: `DISCORD_WEBHOOK_URL`
- Secret: Discordから取得したWebhook URL

### 2-3. 手動実行でテスト

1. リポジトリの **Actions** タブを開く
2. 左側のワークフロー一覧から **Economic Calendar Notification** を選択
3. 右上の **Run workflow** → **Run workflow** をクリック
4. ワークフローが完了するまで待つ（緑チェックマークが表示される）
5. Discordチャンネルで通知を確認

### 2-4. 自動実行の確認

毎週土曜日22:00 (JST)に自動実行されます。次の土曜日まで待って確認してください。

## ✅ 完了！

これで設定は完了です。毎週自動で翌週の重要経済指標がDiscordに投稿されます。

## 🔧 トラブルシューティング

### ローカル実行でエラーが出る場合
- `.env`ファイルが正しく作成されているか確認
- APIキーとWebhook URLが正しいか確認
- 仮想環境が正しく作成されているか確認（`venv`フォルダの存在）

### GitHub Actionsでエラーが出る場合
- GitHub Secretsが正しく設定されているか確認
- ActionsタブでエラーログをチェックSyntax error? 
- Finnhub APIの利用制限を超えていないか確認

詳細は[README.md](README.md)を参照してください。
