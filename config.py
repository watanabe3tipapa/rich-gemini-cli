"""
設定管理とユーティリティ関数
"""

import os
import logging
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# ログ設定
def setup_logging(level: str = "INFO") -> None:
    """ログ設定を初期化"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('gemini_cli.log'),
            logging.StreamHandler()
        ]
    )

@dataclass
class AppConfig:
    """アプリケーション設定"""
    gemini_api_key: Optional[str] = None
    app_name: str = "Gemini Chat CLI"
    app_version: str = "0.1.0"
    max_message_length: int = 1000
    max_history_length: int = 100
    log_level: str = "INFO"
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        """環境変数から設定を読み込み"""
        load_dotenv()
        
        return cls(
            gemini_api_key=os.getenv("GEMINI_API_KEY"),
            app_name=os.getenv("APP_NAME", "Gemini Chat CLI"),
            app_version=os.getenv("APP_VERSION", "0.1.0"),
            max_message_length=int(os.getenv("MAX_MESSAGE_LENGTH", "1000")),
            max_history_length=int(os.getenv("MAX_HISTORY_LENGTH", "100")),
            log_level=os.getenv("LOG_LEVEL", "INFO")
        )
    
    def is_valid(self) -> bool:
        """設定が有効かどうかをチェック"""
        return bool(self.gemini_api_key and len(self.gemini_api_key) > 0)

def validate_api_key(api_key: str) -> bool:
    """APIキーの形式を検証"""
    if not api_key:
        return False
    
    # Gemini APIキーは通常、AIzaで始まる
    if not api_key.startswith("AIza"):
        return False
    
    # 適切な長さかチェック（概算）
    if len(api_key) < 30:
        return False
    
    return True

def get_config() -> AppConfig:
    """設定を取得"""
    config = AppConfig.from_env()
    setup_logging(config.log_level)
    return config 