# File Monitor Library

A cross-platform file monitoring and integrity verification tool with real-time alerts.

## Features

- Real-time file change detection
- SHA-256 file integrity check
- Email alert support
- Windows and Linux/macOS support
- Audit log stubs for advanced access tracking

## Usage

```python
from file_monitor import FileMonitor

monitor = FileMonitor(path="/etc", alert_callback=print)
monitor.start()
```
