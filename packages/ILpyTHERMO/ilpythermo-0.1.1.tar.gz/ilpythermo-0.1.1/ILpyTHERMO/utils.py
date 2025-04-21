from collections import defaultdict

def standardize_headers(headers):
    """Standardize column headers"""
    standardized = []
    for header in headers:
        header = str(header).strip().lower()
        standardized.append(header)
    return standardized

def deduplicate_columns(columns):
    """Remove duplicate column names"""
    counts = defaultdict(int)
    new_columns = []
    for col in columns:
        if counts[col]:
            new_columns.append(f"{col}.{counts[col]}")
        else:
            new_columns.append(col)
        counts[col] += 1
    return new_columns
