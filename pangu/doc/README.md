# 🐍 Pangu Python Project

This project uses **Conda**, `Makefile`, and modular shell scripts to manage environment, dependencies, and testing clean-up.

## 🔧 Setup

### 1. Install Conda (Miniconda or Anaconda)

[Download Miniconda](https://docs.conda.io/en/latest/miniconda.html)

### 2. Initialize Environment

```bash
make init-env
```

### 3. Activate Environment

```bash
conda activate proj-pangu-env
```

### 4. Install Dependencies (dev + tools)

```bash
make install-deps
```

## 🧪 Testing

```bash
pytest
```

## 🧹 Clean Cache

```bash
make clear-cache
```

## 📂 Project Structure

```
.
├── Makefile
├── requirements.txt
├── shell/               # Shell utilities
├── pangu/               # Main Python package
└── tests/               # Test modules
```

---

## ✅ Commands Summary

| Command | Description |
|--------|-------------|
| `make init-env` | Create conda environment |
| `make activate-env` | Show activation instructions |
| `make install-deps` | Install pip + dev tools |
| `make clear-cache` | Clear Python + pytest cache |
