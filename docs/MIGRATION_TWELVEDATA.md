# Finnhub から Twelve Data への移行ガイド

## 移行理由

Finnhub無料プランでは Economic Calendar API へのアクセスが制限されているため、Twelve Data APIに移行しました。

## 変更内容

### 1. APIサービスの変更

| 項目 | 変更前 (Finnhub) | 変更後 (Twelve Data) |
|------|------------------|---------------------|
| サービス | Finnhub | Twelve Data |
| エンドポイント | `/api/v1/calendar/economic` | `/economic_calendar` |
| 無料プラン制限 | 60 calls/min | 800 calls/day |
| 重要度キー | `impact: "high"` | `importance: "High"` |
| 予想値キー | `estimate` | `forecast` |
| 前回値キー | `previous` | `previous` |

### 2. 環境変数の変更

**変更前:**
```
FINNHUB_API_KEY=your_api_key
```

**変更後:**
```
TWELVEDATA_API_KEY=your_api_key
```

### 3. 移行手順

#### ローカル環境

1. Twelve Data APIキーを取得
   - https://twelvedata.com/ にアクセス
   - 無料アカウント作成
   - ダッシュボードからAPIキー取得

2. `.env`ファイルを更新
   ```bash
   # 古いキーをコメントアウト or 削除
   # FINNHUB_API_KEY=xxx
   
   # 新しいキーを追加
   TWELVEDATA_API_KEY=your_twelvedata_api_key_here
   DISCORD_WEBHOOK_URL=your_webhook_url_here
   ```

3. 動作確認
   ```bash
   ./run_local.sh
   ```

#### GitHub Actions

1. GitHub Secretsを更新
   - リポジトリの Settings → Secrets and variables → Actions
   - `FINNHUB_API_KEY` を削除（または残しておいてOK）
   - `TWELVEDATA_API_KEY` を新規作成

2. 最新コードをプッシュ
   ```bash
   git add .
   git commit -m "Migrate from Finnhub to Twelve Data API"
   git push
   ```

3. 手動実行でテスト
   - Actions タブから手動実行

## Twelve Data の利点

✅ **無料プランで経済カレンダーにアクセス可能**  
✅ **800 API calls/day（週1回なら十分）**  
✅ **レスポンスが読みやすい JSON 形式**  
✅ **グローバルな経済指標に対応**  

## トラブルシューティング

### エラー: "You don't have access to this resource."

→ Twelve Data APIキーを正しく設定しているか確認してください

### データが取得できない

→ 無料プランの制限（800 calls/day）を超えていないか確認

### 指標が0件

→ 翌週に重要度「High」の指標がない場合は正常な動作です

## ロールバック方法

万が一、Finnhubに戻したい場合:

1. `git revert` で以前のコミットに戻す
2. `.env` と GitHub Secrets を Finnhub用に戻す

ただし、Finnhub無料プランでは Economic Calendar API が使用できないため、推奨しません。
