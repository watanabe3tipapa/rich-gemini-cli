"""
設定管理とユーティリティ関数

このモジュールは、アプリケーションの設定管理、ログ設定、
APIキー検証などの共通機能を提供します。
"""

import os
import logging
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv


def setup_logging(level: str = "INFO", log_file: str = "gemini_cli.log") -> None:
    """
    ログ設定を初期化
    
    Args:
        level: ログレベル (DEBUG, INFO, WARNING, ERROR)
        log_file: ログファイル名
    """
    # ログディレクトリを作成
    log_path = Path(log_file)
    log_path.parent.mkdir(exist_ok=True)
    
    # 既存のハンドラーをクリア
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )


@dataclass
class AppConfig:
    """
    アプリケーション設定クラス
    
    環境変数から設定を読み込み、デフォルト値を提供します。
    """
    gemini_api_key: Optional[str] = None
    app_name: str = "Rich Gemini CLI"
    app_version: str = "0.2.0"
    max_message_length: int = 2000
    max_history_length: int = 50
    log_level: str = "INFO"
    log_file: str = "gemini_cli.log"
    api_timeout: int = 30
    temperature: float = 0.7
    max_tokens: int = 2048
    
    # 生成パラメータ
    generation_config: dict = field(default_factory=lambda: {
        "temperature": 0.7,
        "topK": 40,
        "topP": 0.95,
        "maxOutputTokens": 2048,
    })
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        """
        環境変数から設定を読み込み
        
        Returns:
            AppConfig: 設定インスタンス
        """
        load_dotenv()
        
        config = cls(
            gemini_api_key=os.getenv("GEMINI_API_KEY"),
            app_name=os.getenv("APP_NAME", "Rich Gemini CLI"),
            app_version=os.getenv("APP_VERSION", "0.2.0"),
            max_message_length=int(os.getenv("MAX_MESSAGE_LENGTH", "2000")),
            max_history_length=int(os.getenv("MAX_HISTORY_LENGTH", "50")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_file=os.getenv("LOG_FILE", "gemini_cli.log"),
            api_timeout=int(os.getenv("API_TIMEOUT", "30")),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("MAX_TOKENS", "2048")),
        )
        
        # 生成パラメータを更新
        config.generation_config.update({
            "temperature": config.temperature,
            "maxOutputTokens": config.max_tokens,
        })
        
        return config
    
    def is_valid(self) -> bool:
        """
        設定が有効かどうかをチェック
        
        Returns:
            bool: 設定が有効な場合True
        """
        return bool(
            self.gemini_api_key 
            and len(self.gemini_api_key.strip()) > 0
            and validate_api_key(self.gemini_api_key)
        )
    
    def validate_settings(self) -> list[str]:
        """
        設定の詳細検証
        
        Returns:
            list[str]: エラーメッセージのリスト
        """
        errors = []
        
        if not self.gemini_api_key:
            errors.append("GEMINI_API_KEY が設定されていません")
        elif not validate_api_key(self.gemini_api_key):
            errors.append("GEMINI_API_KEY の形式が正しくありません")
        
        if self.max_message_length < 1:
            errors.append("MAX_MESSAGE_LENGTH は1以上である必要があります")
        
        if self.max_history_length < 1:
            errors.append("MAX_HISTORY_LENGTH は1以上である必要があります")
        
        if not 0.0 <= self.temperature <= 2.0:
            errors.append("TEMPERATURE は0.0から2.0の間である必要があります")
        
        if self.max_tokens < 1:
            errors.append("MAX_TOKENS は1以上である必要があります")
        
        return errors


def validate_api_key(api_key: str) -> bool:
    """
    APIキーの形式を検証
    
    Args:
        api_key: 検証するAPIキー
        
    Returns:
        bool: APIキーが有効な場合True
    """
    if not api_key or not isinstance(api_key, str):
        return False
    
    api_key = api_key.strip()
    
    # Gemini APIキーは通常、AIzaで始まる
    if not api_key.startswith("AIza"):
        return False
    
    # 適切な長さかチェック（概算）
    if len(api_key) < 30 or len(api_key) > 100:
        return False
    
    # 英数字とハイフン、アンダースコアのみ許可
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")
    if not all(c in allowed_chars for c in api_key):
        return False
    
    return True


def get_config() -> AppConfig:
    """
    設定を取得し、ログを初期化
    
    Returns:
        AppConfig: アプリケーション設定
    """
    config = AppConfig.from_env()
    setup_logging(config.log_level, config.log_file)
    return config


def create_sample_env() -> None:
    """
    サンプル.envファイルを作成
    """
    sample_content = """# Gemini API設定
# Google AI Studio (https://makersuite.google.com/app/apikey) から取得してください
GEMINI_API_KEY=your_gemini_api_key_here

# アプリケーション設定
APP_NAME=Rich Gemini CLI
APP_VERSION=0.2.0

# 動作設定
MAX_MESSAGE_LENGTH=2000
MAX_HISTORY_LENGTH=50
LOG_LEVEL=INFO
LOG_FILE=gemini_cli.log
API_TIMEOUT=30

# AI生成パラメータ
TEMPERATURE=0.7
MAX_TOKENS=2048
"""
    
    env_path = Path(".env")
    if not env_path.exists():
        env_path.write_text(sample_content, encoding='utf-8')
        print(f"サンプル.envファイルを作成しました: {env_path.absolute()}")
    else:
        print(".envファイルは既に存在します") 