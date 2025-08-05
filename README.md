# 🤖 Rich Gemini CLI

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**美しく、パワフルで、使いやすい Gemini AI チャットインターフェース**

Richライブラリを活用した洗練されたコンソール表示と、Google Gemini AIの強力な対話機能を組み合わせた、次世代のコマンドラインチャットアプリケーションです。

## ✨ 主な特徴

### 🎨 **美しいユーザーインターフェース**
- 🌈 Richライブラリによる色彩豊かなコンソール表示
- 📊 構造化されたテーブルとパネル表示
- 🔄 アニメーション付きプログレスインジケーター
- 📝 Markdown形式のレスポンス表示

### 🛡️ **堅牢なシステム**
- 🔒 包括的なエラーハンドリング
- 📋 詳細なログ機能
- ✅ APIキー形式の自動検証
- ⚙️ 柔軟な設定管理システム

### 🚀 **高度な機能**
- 💾 インテリジェントな会話履歴管理
- 🎛️ カスタマイズ可能なAI生成パラメータ
- 📊 リアルタイムステータス表示
- 🔧 豊富なコマンドラインオプション

## 📋 システム要件

- **Python**: 3.10以上
- **OS**: Windows, macOS, Linux
- **メモリ**: 最小 256MB RAM
- **ネットワーク**: インターネット接続（Gemini API用）

## 🛠️ インストール

### 方法1: uvを使用（推奨）

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/rich-gemini-cli.git
cd rich-gemini-cli

# 依存関係のインストール
uv sync

# アプリケーションの実行
uv run python main.py
```

### 方法2: pipを使用

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/rich-gemini-cli.git
cd rich-gemini-cli

# 開発モードでインストール
pip install -e .

# アプリケーションの実行
python main.py
# または
gemini-cli
```

## 🔑 セットアップ

### 1. Gemini APIキーの取得

1. [Google AI Studio](https://makersuite.google.com/app/apikey) にアクセス
2. Googleアカウントでサインイン
3. 「Create API Key」をクリック
4. 生成されたAPIキーをコピー（`AIza...`で始まる文字列）

### 2. 環境設定

```bash
# 設定ファイルをコピー
cp env.example .env

# .envファイルを編集してAPIキーを設定
nano .env  # または任意のエディタ
```

**.envファイルの例:**
```env
GEMINI_API_KEY=AIzaSyC...your_actual_api_key_here
MAX_MESSAGE_LENGTH=2000
MAX_HISTORY_LENGTH=50
TEMPERATURE=0.7
LOG_LEVEL=INFO
```

## 🚀 使用方法

### 基本的な使い方

```bash
# アプリケーションを起動
python main.py

# 質問を入力
👤 あなた: こんにちは！今日の天気はどうですか？

# Gemini AIが回答
🤖 Gemini: こんにちは！申し訳ございませんが、私はリアルタイムの天気情報に...
```

### 利用可能なコマンド

| コマンド | 説明 |
|---------|------|
| `/exit`, `exit`, `quit` | アプリケーションを終了 |
| `/clear` | 会話履歴をクリア |
| `/help`, `help` | ヘルプメッセージを表示 |
| `/status` | 現在の設定とステータスを表示 |

### 高度な使用例

```bash
# 開発モードで起動（詳細ログ）
LOG_LEVEL=DEBUG python main.py

# カスタム設定で起動
MAX_MESSAGE_LENGTH=5000 TEMPERATURE=1.2 python main.py

# 特定の設定ファイルを使用
cp custom.env .env && python main.py
```

## ⚙️ 設定オプション

### 環境変数一覧

| 変数名 | デフォルト値 | 説明 |
|--------|-------------|------|
| `GEMINI_API_KEY` | - | **必須** Gemini APIキー |
| `MAX_MESSAGE_LENGTH` | 2000 | 1回のメッセージの最大文字数 |
| `MAX_HISTORY_LENGTH` | 50 | 保持する会話履歴の最大数 |
| `TEMPERATURE` | 0.7 | AI創造性パラメータ (0.0-2.0) |
| `MAX_TOKENS` | 2048 | 最大出力トークン数 |
| `API_TIMEOUT` | 30 | API呼び出しタイムアウト（秒） |
| `LOG_LEVEL` | INFO | ログレベル (DEBUG/INFO/WARNING/ERROR) |
| `LOG_FILE` | gemini_cli.log | ログファイル名 |

### AI生成パラメータの調整

```env
# 創造的な回答を得たい場合
TEMPERATURE=1.2
MAX_TOKENS=4096

# 一貫性を重視したい場合
TEMPERATURE=0.3
MAX_TOKENS=1024

# バランス型（推奨）
TEMPERATURE=0.7
MAX_TOKENS=2048
```

## 📊 ログとモニタリング

### ログファイルの確認

```bash
# リアルタイムでログを監視
tail -f gemini_cli.log

# エラーログのみを表示
grep ERROR gemini_cli.log

# 今日のログを表示
grep "$(date +%Y-%m-%d)" gemini_cli.log
```

### ステータス確認

アプリケーション内で `/status` コマンドを使用すると、現在の設定と統計情報を確認できます。

## 🔧 トラブルシューティング

### よくある問題と解決方法

#### 1. APIキーエラー
```
❌ エラー: APIキーの形式が正しくありません
```
**解決方法:**
- APIキーが `AIza` で始まっているか確認
- APIキーに不要な空白や改行がないか確認
- Google AI Studioで新しいAPIキーを生成

#### 2. ネットワークエラー
```
❌ ネットワークエラー: URLError
```
**解決方法:**
- インターネット接続を確認
- ファイアウォール設定を確認
- プロキシ設定が必要な場合は環境変数を設定

#### 3. 依存関係エラー
```
❌ モジュールのインポートに失敗しました
```
**解決方法:**
```bash
# 依存関係を再インストール
pip install -e .
# または
uv sync
```

#### 4. 設定ファイルの問題
```bash
# 設定をリセット
rm .env
cp env.example .env
# APIキーを再設定
```

### デバッグモード

詳細な診断情報が必要な場合：

```bash
# デバッグモードで起動
LOG_LEVEL=DEBUG python main.py

# または環境変数として設定
export LOG_LEVEL=DEBUG
python main.py
```

## 🎯 パフォーマンス最適化

### 推奨設定

```env
# 高速レスポンス重視
MAX_MESSAGE_LENGTH=1000
MAX_TOKENS=1024
TEMPERATURE=0.5

# 高品質回答重視
MAX_MESSAGE_LENGTH=3000
MAX_TOKENS=4096
TEMPERATURE=0.8

# バランス型（推奨）
MAX_MESSAGE_LENGTH=2000
MAX_TOKENS=2048
TEMPERATURE=0.7
```

## 🤝 開発に参加

### 開発環境のセットアップ

```bash
# 開発用依存関係をインストール
pip install -e ".[dev]"

# コード品質チェック
black .
isort .
flake8 .
mypy .

# テスト実行
pytest
```

### コントリビューション

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🙏 謝辞

- [Google Gemini AI](https://ai.google.com/) - 強力なAI機能
- [Rich](https://github.com/Textualize/rich) - 美しいコンソール表示
- [Python](https://python.org/) - 素晴らしいプログラミング言語

## 📞 サポート

- 🐛 **バグ報告**: [Issues](https://github.com/yourusername/rich-gemini-cli/issues)
- 💡 **機能要望**: [Discussions](https://github.com/yourusername/rich-gemini-cli/discussions)
- 📧 **直接連絡**: example@example.com

---

<div align="center">

**Rich Gemini CLI で、AI との対話をより豊かに！** 🚀

[⭐ Star this repo](https://github.com/yourusername/rich-gemini-cli) | [🍴 Fork](https://github.com/yourusername/rich-gemini-cli/fork) | [📝 Report Issues](https://github.com/yourusername/rich-gemini-cli/issues)

</div>
