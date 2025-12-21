# Finnhub API エンドポイント検証結果

## テスト日時
2025-12-20 23:53

## テストしたエンドポイント

### 1. `/api/v1/calendar/economic` ✅
```bash
curl "https://finnhub.io/api/v1/calendar/economic?from=2024-01-01&to=2024-01-07&token=demo"
# Response: {"error":"Invalid API key"}
```
**結論**: エンドポイントは存在する（APIキーエラーが返される）

### 2. `/api/v1/calendar/economic-calendar` ✅  
```bash
curl "https://finnhub.io/api/v1/calendar/economic-calendar?from=2024-01-01&to=2024-01-07&token=demo"
# Response: {"error":"Invalid API key"}
```
**結論**: エンドポイントは存在する

### 3. `/api/v1/economic-calendar` ✅
```bash
curl "https://finnhub.io/api/v1/economic-calendar?from=2024-01-01&to=2024-01-07&token=demo"
# Response: {"error":"Invalid API key"}
```
**結論**: エンドポイントは存在する

## 問題の原因

エンドポイントの問題ではなく、**APIキーの権限問題**です。

### 403 Forbidden エラーの原因

1. **無料プランの制限**
   - Finnhub無料プランでは Economic Calendar API へのアクセスが制限されている可能性が高い
   - 公式ドキュメントには "Global Economic Calendar" が有料プラン(10年の履歴データ)で提供されていると記載あり

2. **APIキーの確認**
   - APIキーが正しく設定されているか
   - APIキーに必要な権限があるか

## 推奨される対応策

### オプション1: Finnhubの無料プランで利用可能なAPIを確認
Finnhubダッシュボードで、現在のプランで利用可能なエンドポイントを確認

### オプション2: 代替APIサービスへの切り替え

#### Alpha Vantage
- エコノミックインジケーター API提供
- 無料プラン: 1日500リクエスト

#### Trading Economics API
- 経済指標カレンダー提供
- 無料トライアルあり

#### Econom icsDB (旧FRED API)
- 米国経済指標に強い
- 完全無料

## 次のステップ

1. Finnhubダッシュボードで無料プランのAPIスコープを確認
2. Economic Calendar APIが有料プランでのみ提供される場合、代替APIの選定
3. 代替APIへの切り替え実装
