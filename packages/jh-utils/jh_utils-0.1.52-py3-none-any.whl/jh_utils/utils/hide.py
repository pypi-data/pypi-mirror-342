
def postgresql_snippet(table_name):
    query = f"""select column_name, data_type, character_maximum_length, column_default, is_nullable
    from INFORMATION_SCHEMA.COLUMNS where table_name = '{table_name}';"""
    return query
