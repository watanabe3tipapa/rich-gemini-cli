#!/usr/bin/env python3
"""
Rich Gemini CLI - エントリーポイント

このファイルは、Rich Gemini CLIアプリケーションのメインエントリーポイントです。
アプリケーションの起動と基本的なエラーハンドリングを担当します。
"""

import sys
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from gemini import main as gemini_main
except ImportError as e:
    print(f"❌ モジュールのインポートに失敗しました: {e}")
    print("必要な依存関係がインストールされているか確認してください。")
    print("pip install -e . または uv sync を実行してください。")
    sys.exit(1)


def main() -> None:
    """
    アプリケーションのメインエントリーポイント
    
    このファンクションは、Gemini CLIアプリケーションを起動し、
    基本的なエラーハンドリングを提供します。
    """
    try:
        gemini_main()
    except KeyboardInterrupt:
        print("\n👋 アプリケーションが中断されました。")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 予期しないエラーが発生しました: {e}")
        print("詳細なエラー情報はログファイル (gemini_cli.log) を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
