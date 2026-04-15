# 🤖 Rich Gemini CLI

Richライブラリを用いた美しいフォーマットのテキストと、Gemini API/Ollamaを利用して応答を問い合わせるためのコマンドラインインターフェースです。

## ✨ 特徴

- Gemini AI / Ollama との対話型チャット
- プロバイダ選択メニュー
- Richによるフォーマットを適用したコマンドラインインターフェース
- ストリーミング出力対応（Ollama）

## 📋 必要条件

- Python 3.10+
- uv（推奨）

## 🛠️ セットアップ

### 1. リポジトリをクローンします

```bash
git clone https://github.com/yourusername/rich-gemini-cli.git
cd rich-gemini-cli
```

### 2. 依存関係のインストール

```bash
uv sync
```

### 3. Gemini APIキーの取得（Geminiを使用する場合）

1. [Google AI Studio](https://aistudio.google.com/app/apikey) にアクセス
2. Googleアカウントでログイン
3. APIキーを作成
4. 作成されたAPIキーをコピー

### 4. 環境変数の設定

```bash
# .envファイルを作成
cp env.example .env

# .envファイルを編集してAPIキーを設定
nano .env
```

### 5. Ollamaの設定（Ollamaを使用する場合）

```bash
# Ollamaをインストール
brew install ollama

# モデルをダウンロード
ollama pull minimax:2.7-cloud

# Ollamaを起動
ollama serve
```

## 🚀 使い方

### 起動方法

```bash
# メニューから選択
./run.sh

# または直接実行
uv run python gemini.py
```

### コマンド

| コマンド | 説明 |
|---------|------|
| `/exit` | 終了 |
| `/clear` | 履歴をクリア |
| `/help` | ヘルプを表示 |

### プロバイダの切替

起動時にメニューが表示されます：

```
┌─────────────────────────────────────┐
│  🤖 AI Chat CLI                     │
│                                     │
│  [1] Gemini API                     │
│  [2] Ollama (minimax:2.7-cloud)   │
│  [3] 終了                           │
└─────────────────────────────────────┘
```

`1`または`2`を入力してEnterを押してください。

---

## 📝 環境変数

`.env`ファイルで以下を設定できます：

| 変数 | デフォルト値 | 説明 |
|------|-------------|------|
| `GEMINI_API_KEY` | - | Gemini APIキー |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama接続先URL |
| `OLLAMA_MODEL` | `minimax:2.7-cloud` | Ollamaモデル名 |
| `APP_NAME` | `Gemini Chat CLI` | アプリ名 |
| `APP_VERSION` | `0.1.0` | バージョン |
| `MAX_MESSAGE_LENGTH` | `1000` | 最大メッセージ長 |
| `MAX_HISTORY_LENGTH` | `100` | 最大履歴数 |
