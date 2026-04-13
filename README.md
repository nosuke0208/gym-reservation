# ベンチプレス利用予定システム

ジムのベンチプレス利用予定を30分単位で管理するWebアプリです。

**フロントエンド:** https://gym-reservation-psi.vercel.app

## 技術構成

| レイヤー | 技術 |
|---|---|
| フロントエンド | HTML / CSS / JavaScript（Vercel） |
| バックエンド | Python / FastAPI（Render） |
| データベース | PostgreSQL（Supabase） |

## 主な機能

- 30分単位（10:00〜21:30）でのスロット表示・予約
- ユーザー名を入力して予約登録
- 予約のキャンセル（ユーザー名照合あり）
- 週単位のカレンダーナビゲーション（前後2週間）

## API

バックエンドURL: `https://gym-reservation-gh40.onrender.com`

| メソッド | エンドポイント | 説明 |
|---|---|---|
| `GET` | `/reservations?machine=&start=&end=` | 予約一覧取得 |
| `POST` | `/reservations` | 予約登録 |
| `DELETE` | `/reservations/{id}?username=` | 予約キャンセル |

## ローカル開発

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

`.env` に Supabase の接続情報を設定してください。

```
SUPABASE_URL=...
SUPABASE_KEY=...
```
