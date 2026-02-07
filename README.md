# 🧹 Universal Data Cleaner

A Python toolkit that automatically cleans messy CSV and Excel files using AI-powered detection.

## 🎯 What It Does

- **Auto-detects** email and phone columns (even with weird names)
- **Removes empty rows and columns** (configurable thresholds)
- **Consolidates scattered contact info** into clean columns
- **Exports** to CSV, Excel, and JSON formats
- **Documents** everything it did (audit trail)

## 🚀 Quick Start

```python
from data_cleaner import SmartCleaner

# One-line cleaning
cleaner = SmartCleaner('your_messy_file.csv')
cleaner.smart_clean()
