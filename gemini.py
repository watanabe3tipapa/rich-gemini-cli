from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
import os
import json
import urllib.request
import urllib.parse

console = Console()
history = []

def ask_gemini(question: str) -> str:
    """Gemini API に質問を送信し、回答を取得する関数"""
    # 環境変数からAPIキーを取得
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return "[red]エラー: GEMINI_API_KEY環境変数が設定されていません。[/red]\n\n以下の手順でAPIキーを設定してください:\n1. Google AI StudioでAPIキーを取得\n2. export GEMINI_API_KEY='あなたのAPIキー' を実行"
    
    # Gemini API のエンドポイント
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    # リクエストペイロード
    data = {
        "contents": [{
            "parts": [{
                "text": question
            }]
        }]
    }
    
    try:
        # HTTPリクエストを送信
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
        # レスポンスから回答を抽出
        if 'candidates' in result and len(result['candidates']) > 0:
            candidate = result['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                return candidate['content']['parts'][0]['text']
        
        return "[red]Geminiから有効な回答を取得できませんでした。[/red]"
        
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            error_json = json.loads(error_body)
            error_message = error_json.get('error', {}).get('message', 'Unknown error')
            return f"[red]API エラー ({e.code}): {error_message}（APIキーやリクエスト内容を再確認してください）[/red]"
        except Exception:
            return f"[red]HTTP エラー ({e.code}): {error_body}[/red]"
    except Exception as e:
        return f"[red]予期しないエラー: {str(e)}[/red]"

def print_history() -> None:
    console.clear()
    console.print("[bold green]Gemini CLI Chat[/bold green]\n")
    for user, response in history:
        console.print(f"[bold blue]あなた:[/bold blue] {user}")
        console.print(Panel(response, title="[bold magenta]Gemini[/bold magenta]", expand=False))
        console.print()

def main() -> None:
    console.print("[bold green]Gemini CLI Chat[/bold green] (終了: /exit, 履歴クリア: /clear, ヘルプ: /help)\n")
    while True:
        try:
            user_input = Prompt.ask("[bold blue]あなた[/bold blue]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold red]終了します[/bold red]")
            break

        if user_input.strip() in ("/exit", "exit", "quit", "/quit"):
            console.print("[bold red]終了します[/bold red]")
            break
        if user_input.strip() in ("/clear",):
            history.clear()
            console.clear()
            console.print("[bold green]Gemini CLI Chat[/bold green] (終了: /exit, 履歴クリア: /clear, ヘルプ: /help)\n")
            continue
        if user_input.strip() in ("/help", "help"):
            console.print("[bold yellow]/exit[/bold yellow]: 終了, [bold yellow]/clear[/bold yellow]: 履歴クリア, [bold yellow]/help[/bold yellow]: ヘルプ表示\n[bold yellow]質問を入力するとGemini AIが応答します。APIキーが正しいかもご確認ください。[/bold yellow]")
            continue
        if not user_input.strip():
            continue

        with console.status("[bold magenta]Geminiに問い合わせ中...[/bold magenta]", spinner="dots"):
            try:
                response = ask_gemini(user_input)
            except Exception as e:
                response = f"[red]エラー: {e}[/red]"

        history.append((user_input, response))
        print_history()

if __name__ == "__main__":
    main()
    git remote add origin git@github.com:watanabe3tipapa/rich-gemini-cli.git
git branch -M main
git push -u origin main