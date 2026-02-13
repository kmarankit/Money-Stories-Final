def format_annual_table(table):
    headers = table[0]
    rows = table[1:]

    results = []

    for row in rows:
        row_dict = {
            headers[i]: row[i] if i < len(row) else ""
            for i in range(len(headers))
        }
        results.append(row_dict)

    return results
