#!/bin/bash

find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.pyo" -delete 2>/dev/null
find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null
