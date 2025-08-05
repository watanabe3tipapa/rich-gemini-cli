"""
Rich Gemini CLI - メインアプリケーション

Gemini AIとの対話型チャットインターフェースを提供します。
Richライブラリを使用した美しいコンソール表示と、
包括的なエラーハンドリング、ログ機能を備えています。
"""

import json
import logging
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import List, Tuple, Optional
import signal

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text
from rich.markdown import Markdown

from config import get_config, validate_api_key, create_sample_env


# グローバル変数
console = Console()
history: List[Tuple[str, str]] = []
logger = logging.getLogger(__name__)


class GeminiAPIError(Exception):
    """Gemini API関連のカスタム例外"""
    pass


class GeminiClient:
    """Gemini APIクライアントクラス"""
    
    def __init__(self, config):
        self.config = config
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    def _make_request(self, question: str) -> dict:
        """
        Gemini APIにリクエストを送信
        
        Args:
            question: 質問文
            
        Returns:
            dict: APIレスポンス
            
        Raises:
            GeminiAPIError: API呼び出しエラー
        """
        url = f"{self.base_url}?key={self.config.gemini_api_key}"
        
        data = {
            "contents": [{
                "parts": [{
                    "text": question
                }]
            }],
            "generationConfig": self.config.generation_config
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': f'{self.config.app_name}/{self.config.app_version}'
                }
            )
            
            with urllib.request.urlopen(req, timeout=self.config.api_timeout) as response:
                return json.loads(response.read().decode('utf-8'))
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            logger.error(f"HTTP エラー ({e.code}): {error_body}")
            
            try:
                error_json = json.loads(error_body)
                error_message = error_json.get('error', {}).get('message', 'Unknown error')
                raise GeminiAPIError(f"API エラー ({e.code}): {error_message}")
            except json.JSONDecodeError:
                raise GeminiAPIError(f"HTTP エラー ({e.code}): {error_body}")
                
        except urllib.error.URLError as e:
            logger.error(f"URL エラー: {e}")
            raise GeminiAPIError(f"ネットワークエラー: {e}")
            
        except Exception as e:
            logger.error(f"予期しないエラー: {e}")
            raise GeminiAPIError(f"予期しないエラー: {e}")
    
    def ask(self, question: str) -> str:
        """
        Gemini AIに質問を送信
        
        Args:
            question: 質問文
            
        Returns:
            str: AIの回答
        """
        logger.info(f"Gemini APIへの問い合わせ開始: 質問長={len(question)}文字")
        
        try:
            result = self._make_request(question)
            
            # レスポンスから回答を抽出
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    response_text = candidate['content']['parts'][0]['text']
                    logger.info(f"正常に回答を取得: 回答長={len(response_text)}文字")
                    return response_text
            
            logger.warning("有効な回答を取得できませんでした")
            return "[yellow]⚠️ Geminiから有効な回答を取得できませんでした。[/yellow]"
            
        except GeminiAPIError as e:
            return f"[red]❌ {str(e)}[/red]"


def validate_input(user_input: str, config) -> Optional[str]:
    """
    ユーザー入力を検証
    
    Args:
        user_input: ユーザー入力
        config: アプリケーション設定
        
    Returns:
        Optional[str]: エラーメッセージ（問題がない場合はNone）
    """
    if not user_input.strip():
        return "空のメッセージは送信できません。"
    
    if len(user_input) > config.max_message_length:
        return f"メッセージが長すぎます（最大{config.max_message_length}文字）。"
    
    return None


def print_welcome_message(config) -> None:
    """ウェルカムメッセージを表示"""
    welcome_table = Table.grid(padding=1)
    welcome_table.add_column(style="cyan", no_wrap=True)
    welcome_table.add_column()
    
    welcome_table.add_row("🤖", f"[bold green]{config.app_name} v{config.app_version}[/bold green]")
    welcome_table.add_row("📝", "Gemini AIとの対話型チャット")
    welcome_table.add_row("💡", "[dim]コマンド: /exit (終了), /clear (履歴クリア), /help (ヘルプ)[/dim]")
    
    console.print(Panel(welcome_table, title="🚀 ようこそ", border_style="blue"))
    console.print()


def print_help(config) -> None:
    """ヘルプメッセージを表示"""
    help_table = Table(show_header=True, header_style="bold magenta")
    help_table.add_column("コマンド", style="yellow", no_wrap=True)
    help_table.add_column("説明", style="white")
    
    help_table.add_row("/exit, exit, quit", "アプリケーションを終了")
    help_table.add_row("/clear", "チャット履歴をクリア")
    help_table.add_row("/help, help", "このヘルプメッセージを表示")
    help_table.add_row("/status", "現在の設定を表示")
    
    console.print(Panel(help_table, title="📚 ヘルプ", border_style="blue"))
    
    # 設定情報も表示
    settings_text = f"""
[dim]現在の設定:[/dim]
• 最大メッセージ長: {config.max_message_length}文字
• 最大履歴数: {config.max_history_length}件
• API温度: {config.temperature}
• 最大トークン数: {config.max_tokens}
    """
    console.print(Panel(settings_text.strip(), title="⚙️ 設定", border_style="green"))


def print_status(config) -> None:
    """現在のステータスを表示"""
    status_table = Table(show_header=True, header_style="bold cyan")
    status_table.add_column("項目", style="yellow")
    status_table.add_column("値", style="white")
    
    status_table.add_row("アプリ名", config.app_name)
    status_table.add_row("バージョン", config.app_version)
    status_table.add_row("APIキー", "✅ 設定済み" if config.is_valid() else "❌ 未設定")
    status_table.add_row("履歴件数", str(len(history)))
    status_table.add_row("最大メッセージ長", f"{config.max_message_length}文字")
    status_table.add_row("最大履歴数", f"{config.max_history_length}件")
    status_table.add_row("ログレベル", config.log_level)
    
    console.print(Panel(status_table, title="📊 ステータス", border_style="cyan"))


def print_history_display(config) -> None:
    """履歴を美しく表示"""
    console.clear()
    print_welcome_message(config)
    
    if not history:
        console.print("[dim]まだ会話履歴がありません。何か質問してみてください！[/dim]\n")
        return
    
    # 履歴の長さを制限
    display_history = history[-config.max_history_length:] if len(history) > config.max_history_length else history
    
    for i, (user_msg, ai_response) in enumerate(display_history, 1):
        # ユーザーメッセージ
        console.print(f"[bold blue]👤 あなた ({i}/{len(display_history)}):[/bold blue] {user_msg}")
        
        # AIレスポンス（Markdownとして表示）
        try:
            markdown_response = Markdown(ai_response)
            console.print(Panel(
                markdown_response, 
                title="[bold magenta]🤖 Gemini[/bold magenta]", 
                border_style="magenta",
                expand=False
            ))
        except Exception:
            # Markdownパースに失敗した場合は通常のテキストとして表示
            console.print(Panel(
                ai_response, 
                title="[bold magenta]🤖 Gemini[/bold magenta]", 
                border_style="magenta",
                expand=False
            ))
        console.print()


def handle_signal(signum, frame):
    """シグナルハンドラー"""
    logger.info(f"シグナル {signum} を受信しました")
    console.print("\n[yellow]⚠️ 終了シグナルを受信しました。安全に終了します...[/yellow]")
    sys.exit(0)


def main() -> None:
    """メイン関数"""
    # シグナルハンドラーを設定
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    
    try:
        # 設定を読み込み
        config = get_config()
        logger.info(f"{config.app_name} v{config.app_version} を開始")
        
        # 設定検証
        validation_errors = config.validate_settings()
        if validation_errors:
            console.print("[red]❌ 設定エラーが見つかりました:[/red]")
            for error in validation_errors:
                console.print(f"  • {error}")
            console.print("\n[yellow]💡 .envファイルを確認してください。[/yellow]")
            
            # サンプル.envファイルを作成するか確認
            if not Path(".env").exists():
                create_env = Prompt.ask("サンプル.envファイルを作成しますか？", choices=["y", "n"], default="y")
                if create_env.lower() == "y":
                    create_sample_env()
            return
        
        # Geminiクライアントを初期化
        client = GeminiClient(config)
        
        # ウェルカムメッセージを表示
        print_welcome_message(config)
        
        # メインループ
        while True:
            try:
                user_input = Prompt.ask("[bold blue]👤 あなた[/bold blue]")
            except (KeyboardInterrupt, EOFError):
                logger.info("ユーザーによる終了")
                console.print("\n[yellow]👋 さようなら！[/yellow]")
                break
            
            # コマンド処理
            command = user_input.strip().lower()
            
            if command in ("/exit", "exit", "quit", "/quit"):
                logger.info("exitコマンドによる終了")
                console.print("[yellow]👋 さようなら！[/yellow]")
                break
                
            elif command == "/clear":
                logger.info("履歴をクリア")
                history.clear()
                print_history_display(config)
                continue
                
            elif command in ("/help", "help"):
                print_help(config)
                continue
                
            elif command == "/status":
                print_status(config)
                continue
            
            # 入力検証
            error_msg = validate_input(user_input, config)
            if error_msg:
                console.print(f"[red]❌ {error_msg}[/red]")
                continue
            
            # API呼び出し
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold magenta]🤖 Geminiが考えています..."),
                console=console,
                transient=True
            ) as progress:
                progress.add_task("thinking", total=None)
                try:
                    response = client.ask(user_input)
                except Exception as e:
                    logger.error(f"API呼び出しエラー: {e}")
                    response = f"[red]❌ エラーが発生しました: {e}[/red]"
            
            # 履歴に追加
            history.append((user_input, response))
            
            # 履歴の長さを制限
            if len(history) > config.max_history_length:
                history.pop(0)
            
            # 履歴を表示
            print_history_display(config)
    
    except Exception as e:
        logger.error(f"アプリケーションエラー: {e}")
        console.print(f"[red]❌ 予期しないエラーが発生しました: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()