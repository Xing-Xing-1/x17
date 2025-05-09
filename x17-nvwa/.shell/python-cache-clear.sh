#!/bin/bash

echo "[x17-女娲] Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
echo "[x17-女娲] Done."