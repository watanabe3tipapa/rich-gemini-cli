# 🤖 Rich Gemini CLI

Richライブラリを用いた美しいフォーマットのテキストと、Gemini APIを利用して応答を問い合わせるためのコマンドラインインターフェースです。

## ✨ 特徴

  - Gemini AIとの対話型チャット
  - Richによるフォーマットを適用したコマンドラインインターフェース

## 📋 必要条件

  - Python 3.13+
  - Richライブラリ

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
pip install -r requirements.txt
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
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
```

### 5. アプリケーションの実行:

```bash
uv run python main.py
```


## 🚀 使い方（標準）

CLIを実行します:

```bash
uv run python gemini.py
```

---
