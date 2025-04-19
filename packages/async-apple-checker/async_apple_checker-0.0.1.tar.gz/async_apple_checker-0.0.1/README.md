# Async Apple Checker

[![PyPI version](https://badge.fury.io/py/async-apple-checker.svg)](https://pypi.org/project/async-apple-checker/)

An asynchronous Python library to check Apple `.p12` certificates and `.mobileprovision` profiles. It verifies OCSP status, extracts certificate metadata, and analyzes entitlements.

## 🔧 Installation

```bash
pip install async-apple-checker
```

## ✨ Features

- ✅ Extract certificate metadata from `.p12` and `.mobileprovision`
- 🔐 Check OCSP status using Apple CA certificates
- 📱 Analyze provisioning profile entitlements
- ⚡ Caching with `@alru_cache` for performance

## 🚀 Quick Usage

```python
from async_apple_checker import check_p12, check_mobileprovision

# Check a .p12 certificate
with open("certificate.p12", "rb") as f:
    result = await check_p12(f.read(), password="your_password")
    print(result)

# Check a .mobileprovision file
with open("profile.mobileprovision", "rb") as f:
    result = await check_mobileprovision(f.read())
    print(result)
```