# X17 Taiyi

> A lightweight MongoDB interface for structured data orchestration, inspired by 太乙 — the primordial source of all treasures and transformations.

---

## Inspiration

> “太乙者，一也，万化之宗，百宝之源。”

In Chinese mythos, **Taiyi (太乙)** is the origin of all things — a symbol of order, mystery, and elemental power. This module serves as the **resource core** of the X17 system, providing stable, flexible access to structured data for all upper-level modules like *Nvwa*, *Celestial*, and *Xiga*.

---

## Project Overview

**X17 Taiyi** is a lightweight MongoDB wrapper that provides:
- Unified client interface
- Collection and document abstraction
- Environment-aware connection configuration
- Support for human-friendly document access

Taiyi is designed for **developer clarity**, **runtime agility**, and **philosophical beauty** — an engine of memory, logs, and hidden treasure beneath the intelligent cosmos.

---

## Core Features

- **TaiyiClient**: Simple wrapper around `pymongo.MongoClient`, with environment URI and default DB
- **TaiyiDocument**: Basic CRUD class to interact with any MongoDB collection
- **Environment Support**: Uses `X17_MONGO_URI` env var, defaulting to `mongodb://localhost:27017`
- **Expandable**: Designed for future extension into Memory, Vault, Mirror, and Log subsystems

---

## Installation

This module is part of the `x17` ecosystem. Install via:

```bash
pip install x17-taiyi
Requires pymongo>=4.0
```

## License
```
MIT © X17 Studio
Made for all
```
