# snyk-code-playground

Snyk Code(SAST)と Snyk Open Source(依存関係の脆弱性スキャン)の検証用サンプルアプリです。
Flask 製のシンプルな ToDo API(ユーザー登録・ログイン・タスクの CRUD)を実装しています。

## このリポジトリの目的

委託開発における Pull Request 経由でのバックドア混入や、OSS 依存関係の脆弱性を悪用した
バックドアを、CI 上の Snyk チェックで検出できるかを検証するためのプレイグラウンドです。

想定シナリオ:

1. バックドアを含まないベースアプリ(本コミット)を用意する
2. GitHub Actions に Snyk Code(コード自体の静的解析)と Snyk Open Source(依存パッケージの脆弱性スキャン)を組み込む
3. バックドアを仕込んだ Pull Request を作成する
4. CI 上の Snyk チェックが検出・ブロックすることを確認する

## 構成

```
app/
  __init__.py     アプリケーションファクトリ
  models.py       User / Task モデル(パスワードはハッシュ化して保存)
  auth.py         登録・ログイン・ログアウト(セッション認証)
  tasks.py        タスク CRUD(所有者以外はアクセス不可)
  decorators.py   login_required デコレータ
config.py         設定(SECRET_KEY は環境変数必須、ハードコード禁止)
run.py            起動エントリポイント
tests/            pytest によるテスト一式
requirements.txt      本番依存(Snyk Open Source のスキャン対象)
requirements-dev.txt  開発用依存(pytest 等)
```

## セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env  # SECRET_KEY を適当な値に変更する
```

## 起動

```bash
source .venv/bin/activate
SECRET_KEY=<任意の値> python run.py
```

## テスト

```bash
source .venv/bin/activate
SECRET_KEY=test python -m pytest
```

## API

| Method | Path                  | 説明                     | 認証 |
| ------ | --------------------- | ------------------------ | ---- |
| POST   | /api/auth/register    | ユーザー登録              | -    |
| POST   | /api/auth/login       | ログイン                  | -    |
| POST   | /api/auth/logout      | ログアウト                | 要   |
| GET    | /api/tasks            | 自分のタスク一覧          | 要   |
| POST   | /api/tasks            | タスク作成                | 要   |
| PATCH  | /api/tasks/\<id\>     | タスク更新                | 要   |
| DELETE | /api/tasks/\<id\>     | タスク削除                | 要   |
