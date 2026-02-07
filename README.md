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
📊 Real-World Example
Input: 591 business leads with 29 messy columns (email_1, email_2, phone, phone_1, etc.)
Output: 591 clean rows with 12 columns:
email (best email per row)
additional_emails (extras if any)
phone (best phone per row)
additional_phones (extras if any)
Result: 94% email coverage, 97% phone coverage, zero manual work!
🛠️ Technologies
Python 3.12
pandas (data manipulation)
openpyxl (Excel export)
📚 Skills Demonstrated
Data Engineering (ETL pipeline design)
Object-Oriented Programming
Data Quality Assessment
Automated Documentation
Error Handling & Debugging
📁 Files
data_cleaner.py - Main toolkit code
example_usage.ipynb - Colab notebook with examples
sample_output/ - Before/after screenshots
🎓 About This Project
Built as part of "Generative AI for Data Engineers" specialization (IBM/Coursera).
💼 Open to: Data Engineering roles, freelance projects, collaborations
📫 Reach me: [your.email@example.com]
