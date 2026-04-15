from abc import ABC, abstractmethod
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.menu import Menu
import os
import json
import urllib.request
import httpx
import asyncio

console = Console()
history = []


class Provider(ABC):
    @abstractmethod
    def ask(self, question: str, history: list) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


class GeminiProvider(Provider):
    def get_name(self) -> str:
        return "Gemini API"

    def ask(self, question: str, history: list) -> str:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return "[red]エラー: GEMINI_API_KEY環境変数が設定されていません。[/red]\n\n以下の手順でAPIキーを設定してください:\n1. Google AI StudioでAPIキーを取得\n2. export GEMINI_API_KEY='あなたのAPIキー' を実行"

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"

        messages = []
        for user, response in history:
            messages.append({"role": "user", "parts": [{"text": user}]})
            messages.append({"role": "model", "parts": [{"text": response}]})
        messages.append({"role": "user", "parts": [{"text": question}]})

        data = {"contents": messages}

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )

            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))

            if "candidates" in result and len(result["candidates"]) > 0:
                candidate = result["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    return candidate["content"]["parts"][0]["text"]

            return "[red]Geminiから有効な回答を取得できませんでした。[/red]"

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            try:
                error_json = json.loads(error_body)
                error_message = error_json.get("error", {}).get(
                    "message", "不明なエラー"
                )
                return f"[red]API エラー ({e.code}): {error_message}[/red]"
            except Exception:
                return f"[red]HTTP エラー ({e.code}): {error_body}[/red]"
        except Exception as e:
            return f"[red]予期しないエラー: {str(e)}[/red]"


class OllamaProvider(Provider):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def get_name(self) -> str:
        return f"Ollama ({self.model})"

    def ask(self, question: str, history: list) -> str:
        messages = []
        for user, response in history:
            messages.append({"role": "user", "content": user})
            messages.append({"role": "assistant", "content": response})
        messages.append({"role": "user", "content": question})

        try:
            with httpx.Client(timeout=120.0) as client:
                with client.stream(
                    "POST",
                    f"{self.base_url}/api/chat",
                    json={"model": self.model, "messages": messages, "stream": True},
                ) as response:
                    if response.status_code != 200:
                        error_body = response.read().decode("utf-8")
                        return f"[red]Ollama エラー ({response.status_code}): {error_body}[/red]"

                    full_response = ""
                    console.print(
                        f"[bold magenta]{self.get_name()}:[/bold magenta] ", end=""
                    )
                    for line in response.iter_lines():
                        if line.startswith("data: "):
                            line = line[6:]
                        if line == "[DONE]":
                            break
                        if line:
                            try:
                                data = json.loads(line)
                                if "message" in data and "content" in data["message"]:
                                    content = data["message"]["content"]
                                    console.print(content, end="", style="cyan")
                                    full_response += content
                            except json.JSONDecodeError:
                                continue
                    console.print()
                    return (
                        full_response
                        if full_response
                        else "[yellow]空のレスポンスを受け取りました。[/yellow]"
                    )

        except httpx.ConnectError:
            return f"[red]接続エラー: Ollama ({self.base_url}) に接続できません。Ollamaが起動していることを確認してください。[/red]"
        except httpx.TimeoutException:
            return "[red]タイムアウト: レスポンスが時間内に返ってきませんでした。[/red]"
        except Exception as e:
            return f"[red]予期しないエラー: {str(e)}[/red]"


def show_provider_menu() -> int:
    console.clear()
    console.print(
        Panel.fit(
            "[bold cyan]🤖 AI Chat CLI[/bold cyan]\n\n"
            "[1] Gemini API\n"
            "[2] Ollama (minimax:2.7-cloud)\n"
            "[3] 終了",
            title="[bold]プロバイダ選択[/bold]",
            border_style="cyan",
        )
    )

    while True:
        choice = Prompt.ask("\n[bold yellow]選択[/bold yellow] (1-3)", default="1")
        if choice in ("1", "2", "3"):
            return int(choice)
        console.print("[red]無効な選択です。1、2、または3を入力してください。[/red]")


def create_provider(choice: int, config) -> Provider | None:
    if choice == 1:
        return GeminiProvider()
    elif choice == 2:
        return OllamaProvider(config.ollama_base_url, config.ollama_model)
    return None


def print_history(provider_name: str) -> None:
    console.clear()
    console.print(f"[bold green]{provider_name} Chat[/bold green]\n")
    for user, response in history:
        console.print(f"[bold blue]あなた:[/bold blue] {user}")
        console.print(
            Panel(response, title="[bold magenta]AI[/bold magenta]", expand=False)
        )
        console.print()


def main() -> None:
    from config import get_config

    config = get_config()
    choice = show_provider_menu()

    if choice == 3:
        console.print("[bold red]終了します[/bold red]")
        return

    provider = create_provider(choice, config)
    if not provider:
        return

    console.clear()
    console.print(
        f"[bold green]{provider.get_name()} Chat[/bold green] (終了: /exit, 履歴クリア: /clear, ヘルプ: /help)\n"
    )

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
            console.print(
                f"[bold green]{provider.get_name()} Chat[/bold green] (終了: /exit, 履歴クリア: /clear, ヘルプ: /help)\n"
            )
            continue
        if user_input.strip() in ("/help", "help"):
            console.print(
                "[bold yellow]/exit[/bold yellow]: 終了, [bold yellow]/clear[/bold yellow]: 履歴クリア, [bold yellow]/help[/bold yellow]: ヘルプ表示\n[bold yellow]質問を入力するとAIが応答します。[/bold yellow]"
            )
            continue
        if not user_input.strip():
            continue

        with console.status(
            f"[bold magenta]{provider.get_name()}に問い合わせ中...[/bold magenta]",
            spinner="dots",
        ):
            try:
                response = provider.ask(user_input, history)
            except Exception as e:
                response = f"[red]エラー: {e}[/red]"

        history.append((user_input, response))
        print_history(provider.get_name())


if __name__ == "__main__":
    main()
