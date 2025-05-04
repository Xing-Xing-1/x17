#!/bin/bash

find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
find . -type f -name ".coverage" -delete 2>/dev/null
find . -type d -name "__snapshots__" -exec rm -rf {} + 2>/dev/null
