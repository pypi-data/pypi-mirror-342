# Aqago App SDK for Python

Python SDK to instrument applications with Aqago.

## Overview

The Aqago App SDK for Python makes it easy to instrument your applications with
Aqago. It abstracts interacting with the Aqago Device Agent running on your
applications' system.

## Installation

```bash
pip install aqago-app-sdk
```

## Getting Started

### Access Artifacts from an Application

```python
import aqago_app_sdk as aqago

def main():
    artifact = aqago.app("my-application").artifacts["my-file"]
```
