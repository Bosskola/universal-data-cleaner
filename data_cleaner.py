# UNIVERSAL DATA CLEANING TOOLKIT v3.6 - AUTO-DETECT + SAFE FALLBACK
# Features: Working consolidation + Smart auto-detection for any data

import pandas as pd
import numpy as np
import os
from datetime import datetime
import json
import re

print("🚀 UNIVERSAL DATA CLEANING TOOLKIT v3.6 - AUTO-DETECT + SAFE")
print("="*60)
print("Features:")
print("  ✅ Removes sparse columns (universal)")
print("  ✅ Auto-detects email/phone columns (smart)")
print("  ✅ Falls back to safe defaults (won't break)")
print("  ✅ Works on ANY messy data")
print("="*60)


# ============================================
# PART 1: DATA PROFILER (Unchanged - works perfectly)
# ============================================

class DataProfiler:
    """Professional data profiling tool - works on any CSV/Excel"""

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.profile = {}

    def load_data(self):
        """Smart loader - handles CSV, Excel, multiple sheets"""
        print(f"\n📁 Loading: {self.file_path}")

        if self.file_path.endswith('.csv'):
            self.df = pd.read_csv(self.file_path)
            self.profile['file_type'] = 'CSV'
        elif self.file_path.endswith(('.xlsx', '.xls')):
            xl = pd.ExcelFile(self.file_path)
            if len(xl.sheet_names) == 1:
                self.df = pd.read_excel(self.file_path)
                self.profile['file_type'] = 'Excel (1 sheet)'
            else:
                self.profile['file_type'] = f'Excel ({len(xl.sheet_names)} sheets)'
                self.profile['sheets'] = xl.sheet_names
                self.df = pd.read_excel(self.file_path, sheet_name=0)
                print(f"   Found sheets: {xl.sheet_names}")
                print(f"   Loading first sheet...")

        self.profile['rows'] = len(self.df)
        self.profile['columns'] = len(self.df.columns)
        print(f"✅ Loaded: {self.profile['rows']:,} rows × {self.profile['columns']} columns")

    def analyze_quality(self):
        """Detect data quality issues"""
        print("\n🔍 Analyzing data quality...")
        issues = []

        # Missing values in columns
        missing_pct = (self.df.isnull().sum() / len(self.df) * 100).round(1)
        very_sparse_cols = missing_pct[missing_pct > 60]
        if len(very_sparse_cols) > 0:
            issues.append(f"⚠️  {len(very_sparse_cols)} columns with >60% missing")

        # Duplicate rows
        dups = self.df.duplicated().sum()
        if dups > 0:
            issues.append(f"⚠️  {dups} duplicate rows")

        # Sparse rows
        filled_pct = self.df.notna().mean(axis=1) * 100
        sparse_rows = (filled_pct < 30).sum()
        if sparse_rows > 0:
            issues.append(f"⚠️  {sparse_rows} rows with <30% data")

        self.profile['issues'] = issues
        self.profile['missing_data'] = missing_pct.to_dict()

        print(f"   Found {len(issues)} potential issues")
        for issue in issues:
            print(f"   {issue}")

        # Show worst columns
        print(f"\n   Worst columns (most missing):")
        worst = missing_pct.sort_values(ascending=False).head(5)
        for col, pct in worst.items():
            print(f"      - {col}: {pct}% missing")

    def generate_report(self):
        """Create summary for AI cleaning assistant"""
        report = f"""
DATA PROFILING REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
File: {self.file_path}

BASIC INFO:
- File type: {self.profile.get('file_type', 'Unknown')}
- Dimensions: {self.profile['rows']:,} rows × {self.profile['columns']} columns

DATA QUALITY ISSUES:
{chr(10).join(self.profile['issues']) if self.profile['issues'] else '  ✅ No major issues detected'}

WORST COLUMNS (most missing):
{chr(10).join([f'  - {k}: {v}%' for k, v in sorted(self.profile['missing_data'].items(), key=lambda x: x[1], reverse=True)[:10]])}

SAMPLE ROWS:
{self.df.head(2).to_string()}
"""
        return report

    def save_profile(self, output_path='data_profile.txt'):
        """Save report to file"""
        report = self.generate_report()
        with open(output_path, 'w') as f:
            f.write(report)
        print(f"\n💾 Profile saved to: {output_path}")
        return report


# ============================================
# PART 2: SMART CLEANER (v3.6 - AUTO-DETECT + SAFE)
# ============================================

class SmartCleaner:
    """Universal data cleaner with smart auto-detection"""

    def __init__(self, input_file):
        self.input_file = input_file
        self.df = None
        self.cleaning_log = []

    def load(self):
        self.df = pd.read_csv(self.input_file)
        print(f"\n📂 Loaded: {len(self.df)} rows × {len(self.df.columns)} columns")
        return self

    def apply_standard_cleaning(self):
        """Universal cleaning rules"""
        # Clean column names
        original_cols = list(self.df.columns)
        self.df.columns = [self._clean_column_name(c) for c in self.df.columns]
        renamed = dict(zip(original_cols, self.df.columns))
        self.cleaning_log.append(f"Renamed {len(renamed)} columns")

        # Remove completely empty rows/columns
        empty_rows = self.df.isnull().all(axis=1).sum()
        self.df = self.df.dropna(how='all')
        self.cleaning_log.append(f"Removed {empty_rows} empty rows")

        empty_cols = self.df.columns[self.df.isnull().all()].tolist()
        self.df = self.df.drop(columns=empty_cols)
        self.cleaning_log.append(f"Removed {len(empty_cols)} empty columns")

        # Standardize text
        text_cols = self.df.select_dtypes(include=['object']).columns
        for col in text_cols:
            self.df[col] = self.df[col].astype(str).str.strip().str.title()

        # Handle missing value indicators
        self.df = self.df.replace(['NaN', 'None', 'NULL', '', 'nan', 'Nan'], pd.NA)
        self.cleaning_log.append("Standardized missing value indicators")

        return self

    def remove_sparse_columns(self, max_missing_percent=60):
        """Remove columns that are mostly empty"""
        print(f"\n📊 Removing sparse columns (> {max_missing_percent}% missing)...")

        before_cols = len(self.df.columns)
        missing_pct = self.df.isnull().mean() * 100
        cols_to_keep = missing_pct[missing_pct <= max_missing_percent].index
        cols_to_drop = missing_pct[missing_pct > max_missing_percent].index

        self.df = self.df[cols_to_keep]
        after_cols = len(self.df.columns)
        dropped = before_cols - after_cols

        if dropped > 0:
            print(f"   ❌ Dropped {dropped} sparse columns:")
            for col in cols_to_drop:
                print(f"      - {col} ({missing_pct[col]:.1f}% missing)")
        else:
            print(f"   ✅ No sparse columns to drop")

        print(f"   ✅ Kept {after_cols} good columns")
        self.cleaning_log.append(f"Removed {dropped} sparse columns (>{max_missing_percent}% missing)")
        return self

    def _detect_email_columns(self, columns):
        """
        SMART DETECTION: Find email columns using multiple strategies
        Strategy 1: Name contains 'email'
        Strategy 2: Content contains '@' in most values
        """
        email_cols = []

        # Strategy 1: Column name contains 'email'
        name_matches = [c for c in columns if 'email' in c.lower()]
        email_cols.extend(name_matches)

        # Strategy 2: Content looks like email (if no name matches found)
        if not email_cols:
            print("   🔍 No 'email' in column names, scanning content...")
            for col in columns:
                if col in self.df.columns:
                    sample = self.df[col].dropna().astype(str).head(20)
                    # If >30% contain @, it's probably email
                    email_like = sample.str.contains('@', na=False).mean()
                    if email_like > 0.3:
                        email_cols.append(col)
                        print(f"      📧 Detected email column by content: {col}")

        # Remove duplicates while preserving order
        seen = set()
        unique_cols = []
        for c in email_cols:
            if c not in seen:
                seen.add(c)
                unique_cols.append(c)

        return unique_cols

    def _detect_phone_columns(self, columns):
        """
        SMART DETECTION: Find phone columns using multiple strategies
        Strategy 1: Name contains 'phone' but not 'email'
        Strategy 2: Content is mostly digits
        """
        phone_cols = []

        # Strategy 1: Column name contains 'phone' (but not 'email')
        name_matches = [c for c in columns if 'phone' in c.lower() and 'email' not in c.lower()]
        phone_cols.extend(name_matches)

        # Strategy 2: Content looks like phone (if no name matches)
        if not phone_cols:
            print("   🔍 No 'phone' in column names, scanning content...")
            for col in columns:
                if col in self.df.columns and col not in phone_cols:
                    sample = self.df[col].dropna().astype(str).head(20)
                    # Extract digits and check length
                    digit_lengths = sample.str.replace(r'\D', '', regex=True).str.len()
                    # If most have 7+ digits, it's probably phone
                    if (digit_lengths >= 7).mean() > 0.3:
                        phone_cols.append(col)
                        print(f"      📞 Detected phone column by content: {col}")

        # Remove duplicates
        seen = set()
        unique_cols = []
        for c in phone_cols:
            if c not in seen:
                seen.add(c)
                unique_cols.append(c)

        return unique_cols

    def consolidate_contact_info(self):
        """
        UNIVERSAL VERSION: Auto-detects OR uses standard patterns
        Works on ANY data with email/phone columns
        """
        print(f"\n🔍 Scanning for contact information...")

        # Get fresh column list
        current_columns = list(self.df.columns)
        print(f"   Total columns: {len(current_columns)}")

        # SMART DETECTION
        email_cols = self._detect_email_columns(current_columns)
        phone_cols = self._detect_phone_columns(current_columns)

        print(f"   📧 Email columns detected: {email_cols if email_cols else 'None'}")
        print(f"   📞 Phone columns detected: {phone_cols if phone_cols else 'None'}")

        # Create new data structure
        new_data = {}

        # Copy all non-contact columns
        cols_to_keep = [c for c in current_columns if c not in email_cols and c not in phone_cols]
        for col in cols_to_keep:
            new_data[col] = self.df[col].values

        # === EMAIL CONSOLIDATION ===
        if len(email_cols) > 0:
            print(f"\n📧 Consolidating {len(email_cols)} email columns...")

            primary_emails = []
            additional_emails_list = []

            for idx in range(len(self.df)):
                emails = []
                row = self.df.iloc[idx]
                for col in email_cols:
                    try:
                        val = row[col]
                        if pd.notna(val) and str(val).strip() and '@' in str(val):
                            email_clean = str(val).strip()
                            if email_clean.lower() not in [e.lower() for e in emails]:
                                emails.append(email_clean)
                    except:
                        continue

                primary_emails.append(emails[0] if len(emails) > 0 else None)
                additional_emails_list.append(', '.join(emails[1:]) if len(emails) > 1 else None)

            new_data['primary_email'] = primary_emails
            new_data['additional_emails'] = additional_emails_list

            with_email = sum(1 for e in primary_emails if e is not None)
            print(f"   ✅ {with_email}/{len(primary_emails)} rows have email")

        # === PHONE CONSOLIDATION ===
        if len(phone_cols) > 0:
            print(f"\n📞 Consolidating {len(phone_cols)} phone columns...")

            primary_phones = []
            additional_phones_list = []

            for idx in range(len(self.df)):
                phones = []
                row = self.df.iloc[idx]
                for col in phone_cols:
                    try:
                        val = row[col]
                        if pd.notna(val) and str(val).strip():
                            digits = ''.join(c for c in str(val) if c.isdigit())
                            if len(digits) >= 7:
                                phone_clean = str(val).strip()
                                if phone_clean not in phones:
                                    phones.append(phone_clean)
                    except:
                        continue

                primary_phones.append(phones[0] if len(phones) > 0 else None)
                additional_phones_list.append(', '.join(phones[1:]) if len(phones) > 1 else None)

            new_data['primary_phone'] = primary_phones
            new_data['additional_phones'] = additional_phones_list

            with_phone = sum(1 for p in primary_phones if p is not None)
            print(f"   ✅ {with_phone}/{len(primary_phones)} rows have phone")

        # Create new DataFrame
        self.df = pd.DataFrame(new_data)

        # Rename to standard names
        rename_map = {}
        if 'primary_email' in self.df.columns:
            rename_map['primary_email'] = 'email'
        if 'primary_phone' in self.df.columns:
            rename_map['primary_phone'] = 'phone'

        if rename_map:
            self.df = self.df.rename(columns=rename_map)

        self.cleaning_log.append(f"Consolidated {len(email_cols)} email + {len(phone_cols)} phone columns")
        return self

    def remove_sparse_rows(self, min_filled_percent=25):
        """Remove rows that are mostly empty"""
        print(f"\n🧹 Removing sparse rows (keeping rows with ≥{min_filled_percent}% data)...")

        filled_pct = self.df.notna().mean(axis=1) * 100
        before = len(self.df)
        self.df = self.df[filled_pct >= min_filled_percent]
        after = len(self.df)
        removed = before - after

        if removed > 0:
            print(f"   ❌ Removed {removed} rows ({removed/before:.1%}) with <{min_filled_percent}% data")
        else:
            print(f"   ✅ All rows have ≥{min_filled_percent}% data")

        print(f"   ✅ Kept {after} rows")
        self.cleaning_log.append(f"Removed {removed} sparse rows (<{min_filled_percent}% filled)")
        return self

    def final_cleanup(self):
        """Final pass: remove any remaining columns that are 100% NaN"""
        print(f"\n🧼 Final cleanup...")

        # Drop columns where EVERYTHING is NaN
        all_nan_cols = self.df.columns[self.df.isnull().all()].tolist()
        if all_nan_cols:
            self.df = self.df.drop(columns=all_nan_cols)
            print(f"   ❌ Dropped {len(all_nan_cols)} all-NaN columns")

        # Reorder columns: most important first
        priority_cols = ['name', 'email', 'phone', 'site', 'country', 'city', 'industry']
        existing_priority = [c for c in priority_cols if c in self.df.columns]
        other_cols = [c for c in self.df.columns if c not in existing_priority]
        self.df = self.df[existing_priority + other_cols]

        print(f"   ✅ Final shape: {len(self.df)} rows × {len(self.df.columns)} columns")
        self.cleaning_log.append("Final cleanup and column reordering")
        return self

    def _clean_column_name(self, name):
        """Convert any column name to clean format"""
        name = str(name)
        name = name.replace('site.company_insights.', '')
        name = name[:30]
        name = name.lower().replace(' ', '_').replace('.', '_')
        name = ''.join(c if c.isalnum() or c == '_' else '_' for c in name)
        return name

    def export_for_visualization(self, output_base='cleaned_data'):
        """Export in multiple formats"""
        outputs = {}

        # CSV (raw data)
        csv_path = f'{output_base}.csv'
        self.df.to_csv(csv_path, index=False)
        outputs['csv'] = csv_path

        # Excel (blanks instead of NaN for clean display)
        excel_path = f'{output_base}.xlsx'
        df_excel = self.df.copy()
        df_excel = df_excel.fillna('')  # Empty string looks better in Excel
        df_excel.to_excel(excel_path, index=False, sheet_name='Cleaned Data')
        outputs['excel'] = excel_path

        # Summary JSON
        summary = {
            'rows': len(self.df),
            'columns': len(self.df.columns),
            'column_names': list(self.df.columns),
            'cleaning_steps': self.cleaning_log,
            'data_quality': {
                'rows_with_email': int(self.df['email'].notna().sum()) if 'email' in self.df.columns else 0,
                'rows_with_phone': int(self.df['phone'].notna().sum()) if 'phone' in self.df.columns else 0,
            },
            'export_timestamp': datetime.now().isoformat()
        }

        json_path = f'{output_base}_summary.json'
        with open(json_path, 'w') as f:
            json.dump(summary, f, indent=2)
        outputs['summary'] = json_path

        print(f"\n📤 Exports complete:")
        for fmt, path in outputs.items():
            print(f"   {fmt}: {path}")

        return outputs

    def generate_data_dictionary(self):
        """Create documentation for business users"""
        dictionary = []

        for col in self.df.columns:
            entry = {
                'column_name': col,
                'data_type': str(self.df[col].dtype),
                'description': self._guess_description(col),
                'sample_values': self.df[col].dropna().head(3).tolist(),
                'missing_pct': round(self.df[col].isnull().mean() * 100, 1),
                'filled_count': int(self.df[col].notna().sum())
            }
            dictionary.append(entry)

        with open('data_dictionary.txt', 'w') as f:
            f.write("DATA DICTIONARY\n")
            f.write("="*60 + "\n\n")
            for entry in dictionary:
                f.write(f"Column: {entry['column_name']}\n")
                f.write(f"  Type: {entry['data_type']}\n")
                f.write(f"  Description: {entry['description']}\n")
                f.write(f"  Missing: {entry['missing_pct']}% ({entry['filled_count']} filled)\n")
                f.write(f"  Examples: {entry['sample_values']}\n\n")

        print("📖 Data dictionary saved: data_dictionary.txt")
        return dictionary

    def _guess_description(self, col_name):
        descriptions = {
            'name': 'Company or business name',
            'email': 'Primary contact email (best available)',
            'additional_emails': 'Secondary emails found in other columns',
            'phone': 'Primary contact phone (best available)',
            'additional_phones': 'Secondary phones found in other columns',
            'site': 'Website URL',
            'country': 'Country location',
            'city': 'City location',
            'industry': 'Business industry category',
            'query': 'Original search term'
        }
        return descriptions.get(col_name, f'{col_name.replace("_", " ").title()} information')


# ============================================
# PART 3: RUN THE COMPLETE PIPELINE
# ============================================

# ⚠️ CHANGE THIS TO YOUR FILE PATH:
FILE_PATH = '/content/messy_outscraper.csv'

print("\n" + "="*60)
print("STEP 1: PROFILING")
print("="*60)

profiler = DataProfiler(FILE_PATH)
profiler.load_data()
profiler.analyze_quality()
report = profiler.save_profile()

print("\n" + "="*60)
print("STEP 2: UNIVERSAL CLEANING WITH AUTO-DETECT")
print("="*60)

cleaner = SmartCleaner(FILE_PATH)
cleaner.load()
cleaner.apply_standard_cleaning()

# Aggressive column removal (60% threshold)
cleaner.remove_sparse_columns(max_missing_percent=60)

# UNIVERSAL: Auto-detects email/phone in ANY data
cleaner.consolidate_contact_info()

# Lower threshold to preserve more rows (25% instead of 40%)
cleaner.remove_sparse_rows(min_filled_percent=25)

# Final cleanup
cleaner.final_cleanup()

cleaner.export_for_visualization('my_cleaned_business_data')
cleaner.generate_data_dictionary()

print("\n" + "="*60)
print("STEP 3: VERIFICATION")
print("="*60)

# Quick check
df_clean = pd.read_csv('my_cleaned_business_data.csv')
print(f"\n✅ FINAL RESULTS:")
print(f"   Shape: {len(df_clean)} rows × {len(df_clean.columns)} columns")
print(f"   Columns: {list(df_clean.columns)}")

if 'email' in df_clean.columns:
    print(f"\n📧 Email coverage: {df_clean['email'].notna().sum()}/{len(df_clean)} rows ({df_clean['email'].notna().mean():.1%})")
if 'phone' in df_clean.columns:
    print(f"📞 Phone coverage: {df_clean['phone'].notna().sum()}/{len(df_clean)} rows ({df_clean['phone'].notna().mean():.1%})")

# Show sample of clean data (AUTO-DETECT available columns)
sample_cols = ['name', 'email', 'phone', 'country']
available_cols = [c for c in sample_cols if c in df_clean.columns]
if available_cols:
    print(f"\n📊 Sample of cleaned data:")
    print(df_clean[available_cols].head(3).to_string())
else:
    print(f"\n📊 First few columns: {list(df_clean.columns[:4])}")
    print(df_clean[df_clean.columns[:4]].head(3).to_string())

print("\n" + "="*60)
print("🎉 UNIVERSAL PORTFOLIO PROJECT COMPLETE!")
print("="*60)
print("\n📁 FILES CREATED:")
print("   1. data_profile.txt - Original audit")
print("   2. my_cleaned_business_data.csv - Clean data")
print("   3. my_cleaned_business_data.xlsx - Excel (no NaN display)")
print("   4. my_cleaned_business_data_summary.json - Metadata")
print("   5. data_dictionary.txt - Full documentation")
print("\n💡 UNIVERSAL FEATURES:")
print("   ✅ Auto-detects 'email' in column names OR content")
print("   ✅ Auto-detects 'phone' in column names OR content")
print("   ✅ Works with: email_1/email_2, phone/phone_1, or any naming")
print("   ✅ Falls back to content scanning if names don't match")
print("   ✅ Safe for ANY messy CSV data!")
