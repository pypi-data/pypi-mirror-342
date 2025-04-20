import csv
import os
from collections import Counter, defaultdict

def CSVSummarize(path):
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    if not rows:
        print("Empty file!")
        return
    
    print(f"\n📄 Summary of file: {os.path.basename(path)}\n")
    
    header = rows[0]
    data = rows[1:]
    
    num_rows = len(data)
    num_cols = len(header)
    
    print(f"Rows: {num_rows}")
    print(f"Columns: {num_cols}")
    
    print("\nColumn Names:")
    print(header)
    
    columns = {col: [] for col in header}
    
    for row in data:
        for idx, value in enumerate(row):
            if idx < len(header):
                columns[header[idx]].append(value.strip())
    
    try:
        file_size = os.path.getsize(path) / (1024 * 1024)
        print(f"\nFile Size: {file_size:.2f} MB")
    except:
        print("\nFile Size: Unable to determine.")
    
    total_elements = sum(len(col) for col in columns.values())
    estimated_memory = total_elements * 50 / (1024 * 1024)
    print(f"Estimated Data Memory Usage: {estimated_memory:.2f} MB")
    
    null_counts = {col: sum(1 for val in vals if val == '' or val.lower() == 'na' or val.lower() == 'null') for col, vals in columns.items()}
    total_nulls = sum(null_counts.values())
    print(f"\nTotal Null Values: {total_nulls}")
    
    null_cols = {col: round(nulls / len(columns[col]) * 100, 2) for col, nulls in null_counts.items() if nulls > 0}
    if null_cols:
        print("\nColumns with Nulls (%):")
        print(null_cols)
    else:
        print("\nNo missing values found.")
    
    duplicate_rows = num_rows - len(set(tuple(row) for row in data))
    print(f"\nDuplicate Rows: {duplicate_rows}")
    
    print("\nTop 5 Frequent Values (first 3 columns):")
    for col in header[:3]:
        counter = Counter(columns[col])
        top5 = counter.most_common(5)
        print(f"  {col}: {dict(top5)}")
    
    uniques = {col: len(set(vals)) for col, vals in columns.items()}
    print("\nUnique Values per Column:")
    print(uniques)
    
    numeric_cols = []
    categorical_cols = []
    for col, vals in columns.items():
        try:
            _ = [float(v) for v in vals if v != '']
            numeric_cols.append(col)
        except:
            categorical_cols.append(col)
    
    print(f"\nNumeric Columns Count: {len(numeric_cols)}")
    print(f"Categorical Columns Count: {len(categorical_cols)}")
    
    constant_cols = [col for col, vals in columns.items() if len(set(vals)) == 1]
    if constant_cols:
        print("\nColumns with Constant Value:")
        print(constant_cols)
    else:
        print("\nNo constant columns found.")
    
    if numeric_cols:
        print("\nBasic Stats (Numeric Columns):")
        for col in numeric_cols:
            try:
                nums = [float(v) for v in columns[col] if v != '']
                if nums:
                    mean = sum(nums) / len(nums)
                    min_val = min(nums)
                    max_val = max(nums)
                    print(f"  {col} - mean: {round(mean, 2)}, min: {min_val}, max: {max_val}")
            except:
                continue
    
    largest_cols = sorted(columns.items(), key=lambda x: sum(len(str(v)) for v in x[1]), reverse=True)[:3]
    print("\nLargest Columns by Memory:")
    for col, vals in largest_cols:
        size_mb = sum(len(str(v)) for v in vals) / (1024 * 1024)
        print(f"  {col}: {size_mb:.2f} MB")
