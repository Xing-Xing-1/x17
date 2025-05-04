# Makefile for x17-wenchang
PACKAGE_NAME = x17_wenchang
VERSION = 0.1.0
DIST_DIR = dist

.PHONY: all build clean upload check

all: build

build:
	@echo "🔨 Building the package..."
	python3 -m build

clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf $(DIST_DIR) *.egg-info

check:
	@echo "🔍 Checking distribution artifacts..."
	twine check $(DIST_DIR)/*

upload:
	@echo "🚀 Uploading to PyPI..."
	twine upload $(DIST_DIR)/*

release: clean build check upload