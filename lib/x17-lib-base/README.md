# x17-base

**x17-base** is the foundational library in the `x17` software ecosystem, offering reusable building blocks for Python applications. It provides core abstractions and utilities to support cross-platform development, temporal operations, and modular system components. This module powers higher-level projects such as `x17-shuli`, `x17-manjusri`, and `x17-celestial`.

---

## Inspiration
> 万八千岁，开天辟地，阳清为天，阴浊为地，盘古在其中，一日九变

## Features

- **Date & Time Toolkit**  
  - Human-friendly durations, timestamps, and cron expression helpers  
  - Interoperability with `datetime`, `timedelta`, and `relativedelta`

- **Cross-Platform Terminal & Path Utilities**  
  - Shell command wrappers for macOS, Linux, and Windows  
  - Path resolution tools across environments

- **Structured Data Models**  
  - Semi-structured data containers (`SemiStruct`)  
  - Support for export, transformation, and introspection

- **AWS Service Helpers**  
  - Client abstractions for S3, Redshift, EC2, and others  
  - Includes custom waiters and API wrappers

- **Modular Design**  
  - Each component is independently testable and import-safe  
  - Designed for extension and minimal dependencies

---

## Installation

Install from PyPI:

```bash
pip install x17-lib-base
```

