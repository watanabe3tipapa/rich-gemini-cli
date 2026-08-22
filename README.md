# 🤖 Rich AI Chat CLI

Gemini API / Ollamaと対話するためのコマンドラインインターフェースです。Richライブラリによる美しいフォーマットと、ストリーミング出力に対応しています。

## ✨ 概要

このプロジェクトは、ローカル端末からGeminiやOllamaベースのモデルと対話できるシンプルなCLIを提供します。Richを使った見やすいコンソール表示、会話履歴管理、（Ollamaでの）ストリーミング出力などの機能を備えています。

## ✨ 主な特徴

- Gemini API / Ollama との対話型チャット
- 起動時に選択できるプロバイダメニュー
- Richによる整ったコンソール表示
- ストリーミング出力対応（Ollama）
- 会話履歴の管理

## 📋 必要環境

- Python 3.10+
- uv（推奨、依存管理に利用）

※ 詳細な依存関係は pyproject.toml を参照してください。

## 🛠️ セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/watanabe3tipapa/rich-gemini-cli.git
cd rich-gemini-cli
```

### 2. 依存関係をインストール

プロジェクトでは uv を利用した同期方法が案内されています。

```bash
uv sync
```

### 3. 環境変数の設定

.env ファイルを用意して必要な鍵や設定を指定します。

```bash
# .envファイルを作成
cp env.example .env

# .envファイルを編集
nano .env
```

.env に設定する代表的な項目や使い方は次の「環境変数」節を参照してください。

## 🔌 プロバイダ別セットアップ

### Gemini を使用する場合

1. Google AI Studio 等でAPIキーを取得してください（README中に参照リンクがあります）。
2. 取得したAPIキーを `.env` に設定します：

```env
GEMINI_API_KEY=（あなたのAPIキー）
```

### Ollama を使用する場合

1. Ollama をインストール（環境に合わせて導入してください）。README内には macOS の Homebrew コマンド例が記載されています。

```bash
brew install ollama  # macOS の例
# または https://ollama.com を参照
```

2. 必要なモデルをダウンロードします（例）：

```bash
ollama pull minimax:2.7-cloud
```

3. Ollama サーバを起動します：

```bash
ollama serve
```

## 🚀 使い方

### 起動方法

```bash
# メニューから選択して起動するスクリプト例
./run.sh

# または直接実行
uv run python gemini.py
```

### 起動時のメニュー（例）

```
┌─────────────────────────────────────┐
│  🤖 AI Chat CLI                     │
│                                     │
│  [1] Gemini API                     │
│  [2] Ollama (minimax:2.7-cloud)   │
│  [3] 終了                           │
└─────────────────────────────────────┘
```

起動後に `1` または `2` を入力して利用するプロバイダを選んでください。

### 対話中のコマンド

| コマンド | 説明 |
|---------|------|
| `/exit` | 終了 |
| `/clear` | 履歴をクリア |
| `/help` | ヘルプを表示 |

## 📝 環境変数

`.env` ファイルで設定可能な主な変数（README 内の一覧を基に記載）：

| 変数 | デフォルト値 | 説明 |
|------|-------------|------|
| `GEMINI_API_KEY` | - | Gemini APIキー（必要時） |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama接続先URL |
| `OLLAMA_MODEL` | `minimax:2.7-cloud` | Ollamaモデル名 |
| `APP_NAME` | `Gemini Chat CLI` | アプリ名 |
| `APP_VERSION` | `0.1.0` | バージョン |
| `MAX_MESSAGE_LENGTH` | `1000` | 最大メッセージ長 |
| `MAX_HISTORY_LENGTH` | `100` | 最大履歴数 |

## ⚙️ 設定例

```env
# Gemini API（実際のAPIキーを設定してください）
GEMINI_API_KEY=（あなたのAPIキー）

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=minimax:2.7-cloud
```

※ 例に示したキーはダミーです。実運用では秘密情報を公開しないようご注意ください。

## 🔧 トラブルシューティング

### API接続エラー

- Gemini: `.env` に設定した API キーが正しいか確認してください。
- Ollama: `ollama serve` が実行中であることを確認してください。

### モデルが見つからない（Ollama）

```bash
ollama list          # インストール済みモデル一覧
ollama pull <モデル名> # モデルをダウンロード
```

## 📁 主なファイル

リポジトリに含まれる主要なファイル（抜粋）:

- README.md
- pyproject.toml
- gemini.py
- main.py
- run.sh
- env.example
- LICENSE

## 🛠 開発・保守状態

- Python >= 3.10 を対象としています（pyproject.toml による）。
- pyproject.toml の分類情報により、Development Status は "Beta" 相当として扱われています。
- 実行用スクリプトやエントリポイントは pyproject.toml の [project.scripts] に定義されています。

## 📄 ライセンス

本プロジェクトは MIT License の下で配布されています（リポジトリ内の LICENSE ファイルを参照）。

----

問題が発生した場合や改善提案がある場合は、このリポジトリの Issue を利用してください。
