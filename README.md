以下に`README.md`の日本語訳を示します。

# 🤖 Rich Gemini CLI

Richライブラリを用いた美しいフォーマットのテキストと、Gemini APIを利用して応答を問い合わせるためのコマンドラインインターフェースです。

## ✨ 特徴

  - Gemini AIとの対話型チャット
  - Richによるフォーマットを適用したコマンドラインインターフェース

## 📋 必要条件

  - Python 3.13+
  - Richライブラリ

## 🛠️ セットアップ

1.  リポジトリをクローンします:

    ```bash
    git clone https://github.com/yourusername/rich-gemini-cli.git
    cd rich-gemini-cli
    ```

2.  依存関係をインストールします:

  
    ```bash
    uv sync
    ```


3.  Gemini APIキーを環境変数に設定します:

    ```bash
    export GEMINI_API_KEY='your-api-key'
    ```

## 🚀 使い方

CLIを実行します:

```bash
uv run python gemini.py
```