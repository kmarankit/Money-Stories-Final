def select_financial_table(tables):

    annual_tables = []
    quarterly_tables = []

    for table in tables:
        table_type = classify_table(table)

        if table_type == "annual":
            annual_tables.append(table)

        elif table_type == "quarterly":
            quarterly_tables.append(table)

    if annual_tables:
        return "annual", annual_tables[0]

    if quarterly_tables:
        return "quarterly", quarterly_tables[0]

    return None, None
