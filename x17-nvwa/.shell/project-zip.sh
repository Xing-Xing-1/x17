#!/bin/bash

# 用法: ./zip-project.sh [output_name]
# 示例: ./zip-project.sh nvwa-snapshot.zip

DEFAULT_NAME="x17-nvwa-$(date +%Y%m%d-%H%M%S).zip"
OUTPUT_NAME="${1:-$DEFAULT_NAME}"

echo "[x17-女娲] Creating zip archive: $OUTPUT_NAME"

# 压缩前排除以下内容
zip -r "$OUTPUT_NAME" . \
  -x "*.git*" \
  -x "*.DS_Store" \
  -x "__pycache__/*" \
  -x "*.pyc" \
  -x "*.pyo" \
  -x ".pytest_cache/*" \
  -x "dist/*" \
  -x "build/*" \
  -x "*.egg-info/*" \
  -x "*.zip"

echo "[x17-女娲] Archive created: $OUTPUT_NAME"