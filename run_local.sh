#!/bin/bash

# 経済指標Discord自動通知ツール - ローカル実行スクリプト
# 仮想環境のセットアップとスクリプト実行を自動化

set -e  # エラーが発生したら即座に終了

echo "======================================================"
echo "経済指標Discord自動通知ツール - ローカル実行"
echo "======================================================"
echo ""

# 1. 仮想環境の作成（存在しない場合）
if [ ! -d "venv" ]; then
    echo "🔧 仮想環境を作成中..."
    python3 -m venv venv
    echo "✅ 仮想環境を作成しました"
else
    echo "✅ 仮想環境は既に存在します"
fi

# 2. 仮想環境を有効化
echo "🔧 仮想環境を有効化中..."
source venv/bin/activate

# 3. 依存関係のインストール
echo "📦 依存関係をインストール中..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ 依存関係のインストール完了"
echo ""

# 4. .envファイルの確認
if [ ! -f ".env" ]; then
    echo "⚠️  .env ファイルが見つかりません"
    echo ""
    echo "以下の手順で .env ファイルを作成してください:"
    echo "1. .env.example をコピーして .env を作成:"
    echo "   cp .env.example .env"
    echo ""
    echo "2. .env ファイルを開いて、実際の値を入力:"
    echo "   - FINNHUB_API_KEY=実際のAPIキー"
    echo "   - DISCORD_WEBHOOK_URL=実際のWebhook URL"
    echo ""
    echo "======================================================"
    exit 1
fi

echo "✅ .env ファイルが見つかりました"
echo ""

# 5. スクリプトを実行
echo "======================================================"
echo "🚀 スクリプトを実行します..."
echo "======================================================"
echo ""

python src/economic_calendar.py

echo ""
echo "======================================================"
echo "✅ 実行完了"
echo "======================================================"
