#!/bin/bash

echo "[x17-女娲] Running isort..."
isort nvwa tests --skip-glob */.venv/* --skip-glob */.git/* --skip-glob */build/*

echo "[x17-女娲] Running black..."
black nvwa tests  # 自动跳过 .gitignore 中的路径

echo "[x17-女娲] Code formatted successfully."