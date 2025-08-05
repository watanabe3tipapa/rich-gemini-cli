from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
import os
import json
import urllib.request
import urllib.parse
import logging
from typing import List, Tuple
from config import get_config, validate_api_key

console = Console()
history: List[Tuple[str, str]] = []
logger = logging.getLogger(__name__)

def ask_gemini(question: str) -> str:
    """Gemini API に質問を送信し、回答を取得する関数"""
    logger.info(f"Gemini APIへの問い合わせを開始: 質問長={len(question)}文字")
    
    # 設定を取得
    config = get_config()
    
    if not config.is_valid():
        logger.warning("APIキーが設定されていません")
        return "[red]エラー: GEMINI_API_KEY環境変数が設定されていません。[/red]\n\n以下の手順でAPIキーを設定してください:\n1. Google AI StudioでAPIキーを取得\n2. .envファイルを作成してGEMINI_API_KEY='あなたのAPIキー'を設定"
    
    # APIキーの形式を検証
    if not validate_api_key(config.gemini_api_key):
        logger.warning("APIキーの形式が正しくありません")
        return "[red]エラー: APIキーの形式が正しくありません。[/red]\n\nGemini APIキーは通常'AIza'で始まり、30文字以上である必要があります。"
    
    # メッセージ長の制限をチェック
    if len(question) > config.max_message_length:
        logger.warning(f"メッセージが長すぎます: {len(question)} > {config.max_message_length}")
        return f"[red]エラー: メッセージが長すぎます（最大{config.max_message_length}文字）。[/red]"
    
    # Gemini API のエンドポイント
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={config.gemini_api_key}"
    
    # リクエストペイロード
    data = {
        "contents": [{
            "parts": [{
                "text": question
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 2048,
        }
    }
    
    try:
        # HTTPリクエストを送信
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            
        # レスポンスから回答を抽出
        if 'candidates' in result and len(result['candidates']) > 0:
            candidate = result['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                response_text = candidate['content']['parts'][0]['text']
                logger.info(f"Gemini APIから正常に回答を取得: 回答長={len(response_text)}文字")
                return response_text
        
        logger.warning("Geminiから有効な回答を取得できませんでした")
        return "[red]Geminiから有効な回答を取得できませんでした。[/red]"
        
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        logger.error(f"HTTP エラー ({e.code}): {error_body}")
        try:
            error_json = json.loads(error_body)
            error_message = error_json.get('error', {}).get('message', 'Unknown error')
            return f"[red]API エラー ({e.code}): {error_message}（APIキーやリクエスト内容を再確認してください）[/red]"
        except Exception:
            return f"[red]HTTP エラー ({e.code}): {error_body}[/red]"
    except Exception as e:
        logger.error(f"予期しないエラー: {str(e)}")
        return f"[red]予期しないエラー: {str(e)}[/red]"

def print_history() -> None:
    """履歴を表示する関数"""
    console.clear()
    config = get_config()
    console.print(f"[bold green]{config.app_name} v{config.app_version}[/bold green]\n")
    
    # 履歴の長さを制限
    display_history = history[-config.max_history_length:] if len(history) > config.max_history_length else history
    
    for user, response in display_history:
        console.print(f"[bold blue]あなた:[/bold blue] {user}")
        console.print(Panel(response, title="[bold magenta]Gemini[/bold magenta]", expand=False))
        console.print()

def main() -> None:
    """メイン関数"""
    config = get_config()
    logger.info(f"{config.app_name} v{config.app_version} を開始")
    console.print(f"[bold green]{config.app_name} v{config.app_version}[/bold green] (終了: /exit, 履歴クリア: /clear, ヘルプ: /help)\n")
    
    while True:
        try:
            user_input = Prompt.ask("[bold blue]あなた[/bold blue]")
        except (KeyboardInterrupt, EOFError):
            logger.info("ユーザーによる終了")
            console.print("\n[bold red]終了します[/bold red]")
            break

        if user_input.strip() in ("/exit", "exit", "quit", "/quit"):
            logger.info("exitコマンドによる終了")
            console.print("[bold red]終了します[/bold red]")
            break
        if user_input.strip() in ("/clear",):
            logger.info("履歴をクリア")
            history.clear()
            console.clear()
            console.print(f"[bold green]{config.app_name} v{config.app_version}[/bold green] (終了: /exit, 履歴クリア: /clear, ヘルプ: /help)\n")
            continue
        if user_input.strip() in ("/help", "help"):
            console.print(f"[bold yellow]/exit[/bold yellow]: 終了, [bold yellow]/clear[/bold yellow]: 履歴クリア, [bold yellow]/help[/bold yellow]: ヘルプ表示\n[bold yellow]質問を入力するとGemini AIが応答します。APIキーが正しいかもご確認ください。[/bold yellow]\n[dim]最大メッセージ長: {config.max_message_length}文字[/dim]")
            continue
        if not user_input.strip():
            continue

        with console.status("[bold magenta]Geminiに問い合わせ中...[/bold magenta]", spinner="dots"):
            try:
                response = ask_gemini(user_input)
            except Exception as e:
                logger.error(f"ask_gemini関数でエラー: {str(e)}")
                response = f"[red]エラー: {e}[/red]"

        history.append((user_input, response))
        
        # 履歴の長さを制限
        if len(history) > config.max_history_length:
            history.pop(0)
            
        print_history()

if __name__ == "__main__":
    main()