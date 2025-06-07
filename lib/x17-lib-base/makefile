# PyPI package name (from pyproject.toml)
PACKAGE_NAME := $(shell grep '^name' pyproject.toml | head -1 | cut -d '"' -f2)
PACKAGE_ALIAS := 盘古


.PHONY: build clean upload version check all

# ========== General ==========

pre:
	@chmod +x .shell/*.sh
	@echo "[$(PACKAGE_ALIAS)] Prehook executed."

info:
	@echo "[$(PACKAGE_ALIAS)] Name: $(PACKAGE_NAME)"
	@echo "[$(PACKAGE_ALIAS)] Alias: $(PACKAGE_ALIAS)"

version:
	@echo "[$(PACKAGE_ALIAS)] Current version:" $(shell grep '^version' pyproject.toml | head -1 | cut -d '"' -f2)


# ========== Conda ==========
.PHONY: init-conda activate-conda remove-conda

init-conda: pre
	@echo "[$(PACKAGE_ALIAS)] Initializing conda environment for $(PACKAGE_NAME)..."
	@.shell/conda-env-init.sh "$(PACKAGE_NAME)"

activate-conda: pre
	@echo "[$(PACKAGE_ALIAS)] Activating conda environment for $(PACKAGE_NAME)..."
	@echo "[$(PACKAGE_ALIAS)] Use 'conda activate $(PACKAGE_NAME)' to activate manually."

remove-conda: pre
	@echo "[$(PACKAGE_ALIAS)] Removing conda environment for $(PACKAGE_NAME)..."
	@.shell/conda-env-remove.sh "$(PACKAGE_NAME)"

all-conda: init-conda activate-conda

# ========= Python ==========
install-python-deps: pre
	@echo "[$(PACKAGE_ALIAS)] Installing Python dependencies for $(PACKAGE_NAME)..."
	@pip install .

clean-python: pre
	@echo "[$(PACKAGE_ALIAS)] Cleaning Python caches..."
	@.shell/python-cache-clear.sh

clean-pytest: pre
	@echo "[$(PACKAGE_ALIAS)] Cleaning pytest caches..."
	@.shell/pytest-cache-clear.sh

clean-build: pre
	@echo "[$(PACKAGE_ALIAS)] Cleaning build artifacts..."
	@.shell/build-cache-clean.sh

clean-all: clean-python clean-pytest clean-build
	@echo "[$(PACKAGE_ALIAS)] All caches and build artifacts cleaned."

# ========== Build & Upload ==========
pkg-build: pre
	@echo "[$(PACKAGE_ALIAS)] Building $(PACKAGE_NAME)..."
	@.shell/core-package-build.sh

pkg-check: pre
	@echo "[$(PACKAGE_ALIAS)] Checking build artifacts with twine..."
	@.shell/core-package-check.sh

pkg-upload: pre
	@echo "[$(PACKAGE_ALIAS)] Uploading to PyPI..."
	@.shell/core-package-upload.sh

pkg-zip: pre
	@echo "[$(PACKAGE_ALIAS)] Zipping project..."
	@.shell/core-package-zip.sh "$(PACKAGE_NAME)"

pkg-all: pkg-build pkg-check pkg-upload pkg-zip
	@echo "[$(PACKAGE_ALIAS)] Package build, check, and upload completed."

# ========== Test ==========
test: pre
	@echo "[$(PACKAGE_ALIAS)] Running tests..."
	@.shell/pytest-test-run.sh
