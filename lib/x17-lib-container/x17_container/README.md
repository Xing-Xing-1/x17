# x17-lib-container (Codename: Luban)

> A Pythonic Docker runtime wrapper for AI infrastructure — enabling declarative container orchestration, mount management, and image lifecycle control.

---

## 🧠 Inspiration

> “器以载道，工以匠心” —— 名曰“鲁班”，即为构器之神。凡器必有制，凡制必有意。吾辈为 AI 构躯体，始于斯也。

---

## Overview

**x17-lib-container** (codename: *Luban*) is part of the `x17` ecosystem, focused on building a modular container runtime system powered by the Docker Python SDK. It enables programmable deployment of services such as MongoDB, Redis, and AI inference engines, optimized for local development and system automation.

---

## Features

- **Container Lifecycle Control**  
  Start, stop, remove containers with full log streaming, parameter introspection, and health status support.

- **Image Strategy Engine**  
  Pull, build, hybrid, or dry-run modes for fine-grained control of Docker image management.

- **Mount System Abstractions**
  - `MountHost` — Bind local directories
  - `MountVolume` — Manage Docker volumes
  - `MountTmpfs` — Configure tmpfs in-memory mounts  
  Supports permission settings (chmod, uid/gid), auto-create logic, and retention policies.

- **MountGroup Composition**  
  Group and manage multiple mounts under a unified object, exportable to native Docker configurations.

---

## Project Layout

```
x17-lib-container/
├── dockers/
│   ├── container/    # Container runtime control
│   ├── image/        # Image loading, pulling, building
│   ├── mount/        # Mount modules: host, volume, tmpfs, group
│   └── test/         # Unit & integration tests
└── README.md
```

---

## Installation

```bash
# Local development install
pip install -e path/to/x17-lib-container
```

Requires:  
- Python 3.8+  
- `docker` Python SDK

---

## Testing

```bash
pytest dockers/test -v
```

---

## Related Projects

- [`x17-svc-dbmongo`](https://github.com/Xing-Xing-1/x17/tree/main/service/x17-svc-dbmongo): MongoDB auto-deploy service using this library  
- [`x17-base`](https://github.com/Xing-Xing-1/x17/tree/main/lib/x17-lib-base): Shared logging, datetime, path tools

---

## Vision

This project lays the foundation for declaratively building AI runtime environments.  
It is part of a greater system to construct embodied, locally-executable AI agents.

> “Roles are not actors. Containers are not minds. But every mind needs a body.”
