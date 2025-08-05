# 🤖 Rich Gemini CLI

Richライブラリを用いた美しいフォーマットのテキストと、Gemini APIを利用して応答を問い合わせるためのコマンドラインインターフェースです。

## ✨ 特徴

- Gemini AIとの対話型チャット
- Richによるフォーマットを適用したコマンドラインインターフェース
- 設定可能なメッセージ長制限と履歴管理
- 包括的なログ機能
- APIキー形式の検証
- エラーハンドリングの強化

## 📋 必要条件

- Python 3.10+
- Richライブラリ
- python-dotenvライブラリ

## 🛠️ セットアップ

### 1. リポジトリをクローンします:

```bash
git clone https://github.com/yourusername/rich-gemini-cli.git
cd rich-gemini-cli
```

### 2. 依存関係のインストール:

```bash
# uvを使用（推奨）
uv sync

# または pipを使用
pip install -e .
```

### 3. Gemini APIキーの取得:

1. [Google AI Studio](https://makersuite.google.com/app/apikey) にアクセス
2. Googleアカウントでログイン
3. APIキーを作成
4. 作成されたAPIキーをコピー

### 4. 環境変数の設定:

```bash
# .envファイルを作成
cp env.example .env

# .envファイルを編集してAPIキーを設定
# GEMINI_API_KEY=your_actual_api_key_here
```

### 5. アプリケーションの実行:

```bash
# メインエントリーポイント
uv run python main.py

# または直接実行
uv run python gemini.py

# インストール後はコマンドとしても実行可能
gemini-cli
```

## 🚀 使い方

### 基本的な使用方法

CLIを実行すると対話型チャットが開始されます:

```bash
uv run python main.py
```

### 利用可能なコマンド

- `/exit` または `exit`, `quit`, `/quit`: アプリケーションを終了
- `/clear`: チャット履歴をクリア
- `/help` または `help`: ヘルプメッセージを表示

### 設定オプション

`.env`ファイルで以下の設定を変更できます:

- `MAX_MESSAGE_LENGTH`: 1回のメッセージの最大文字数（デフォルト: 1000）
- `MAX_HISTORY_LENGTH`: 保持する履歴の最大数（デフォルト: 100）
- `LOG_LEVEL`: ログレベル（DEBUG, INFO, WARNING, ERROR）

## 📝 ログ機能

アプリケーションは`gemini_cli.log`ファイルにログを出力します。デバッグやトラブルシューティングに活用してください。

## 🔧 トラブルシューティング

### APIキーエラー
- APIキーが正しく設定されているか確認
- APIキーが'AIza'で始まり、30文字以上であることを確認

### ログの確認
- `gemini_cli.log`ファイルでエラーの詳細を確認

---
