def extract_all_tables(markdown: str):
    tables = []
    current_table = []

    for line in markdown.splitlines():
        if "|" in line and "---" not in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            current_table.append(parts)
        else:
            if current_table:
                tables.append(current_table)
                current_table = []

    if current_table:
        tables.append(current_table)

    return tables
