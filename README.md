# 🤖 Rich AI Chat CLI

Gemini API / Ollamaと対話するためのコマンドラインインターフェースです。Richライブラリによる美しいフォーマットと、ストリーミング出力に対応しています。

## ✨ 特徴

- Gemini AI / Ollama との対話型チャット
- プロバイダ選択メニュー（起動時に選択可能）
- Richによる美しいコンソール表示
- ストリーミング出力対応（Ollama）
- 会話履歴の管理

## 📋 必要環境

- Python 3.10+
- uv（推奨）

## 🛠️ セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/watanabe3tipapa/rich-gemini-cli.git
cd rich-gemini-cli
```

### 2. 依存関係をインストール

```bash
uv sync
```

### 3. 環境変数の設定

```bash
# .envファイルを作成
cp env.example .env

# .envファイルを編集
nano .env
```

#### Geminiを使用する場合

1. [Google AI Studio](https://aistudio.google.com/app/apikey) にアクセス
2. APIキーを作成
3. `.env`ファイルに以下を設定：
   ```
   GEMINI_API_KEY=あなたのAPIキー
   ```

#### Ollamaを使用する場合

1. Ollamaをインストール：
   ```bash
   brew install ollama  # macOS
   # または https://ollama.com を参照
   ```

2. モデルをダウンロード：
   ```bash
   ollama pull minimax:2.7-cloud
   ```

3. Ollamaを起動：
   ```bash
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

### 起動時のメニュー

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

### コマンド

| コマンド | 説明 |
|---------|------|
| `/exit` | 終了 |
| `/clear` | 履歴をクリア |
| `/help` | ヘルプを表示 |

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

## ⚙️ 設定例

```env
# Gemini API
GEMINI_API_KEY=AIzaSyC...

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=minimax:2.7-cloud
```

## 🔧 トラブルシューティング

### API接続エラー

- Gemini: APIキーが正しく設定されているか確認
- Ollama: `ollama serve`が実行中か確認

### モデルが見つからない（Ollama）

```bash
ollama list          # インストール済みモデル一覧
ollama pull <モデル名> # モデルをダウンロード
```

## 📄 ライセンス

MIT License
