PACKAGE_NAME = x17_pangu

.PHONY: help build clean upload version check all

help:
	@echo "Usage:"
	@echo "  make build     - Build the package (wheel + sdist)"
	@echo "  make upload    - Upload the package to PyPI (requires twine)"
	@echo "  make clean     - Remove dist/ and build artifacts"
	@echo "  make check     - Run twine check to validate the package"
	@echo "  make version   - Show current version"
	@echo "  make all       - Build, check, and upload"

version:
	@grep '^version' pyproject.toml | head -1

clean:
	rm -rf dist/ build/ *.egg-info

build:
	@echo ">>> Building $(PACKAGE_NAME)..."
	python3 -m build

check:
	@echo ">>> Checking build artifacts with twine..."
	twine check dist/*

upload: build check
	@echo ">>> Uploading to PyPI..."
	twine upload dist/*

all: clean build check upload