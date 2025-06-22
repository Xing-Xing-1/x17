OUTPUT_NAME="$1-$(date +%Y%m%d).zip"
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
