def classify_table(table):
    headers = table[0]
    header_text = " ".join(headers).lower()

    if "balance sheet" in header_text:
        return "balance_sheet"

    if "quarter ended" in header_text:
        return "quarterly"

    if "nine months" in header_text:
        return "quarterly"

    if "previous year ended" in header_text:
        return "quarterly"

    if "fy" in header_text:
        return "annual"

    if "year ended 31 march" in header_text:
        return "annual"

    return "unknown"
