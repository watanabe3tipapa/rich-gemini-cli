#!/bin/bash
# Rich Gemini CLI 起動スクリプト
# 使用例: ./run.sh [gemini|ollama]

PROVIDER=${1:-""}

if [ "$PROVIDER" = "gemini" ]; then
    export DEFAULT_PROVIDER=gemini
elif [ "$PROVIDER" = "ollama" ]; then
    export DEFAULT_PROVIDER=ollama
fi

uv run python gemini.py
