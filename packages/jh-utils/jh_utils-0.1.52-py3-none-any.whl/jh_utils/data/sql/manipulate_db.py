from sqlalchemy import inspect
import sqlalchemy as sa

# create_table_structure, get_tables, drop_table, delete_table, get_top_rows
# get_schemas, create_schema, drop_schema
# apply_delete_to_schema

# ! Table


def create_table_structure(
    pandas_df, table_name, engine, schema, index=False, if_exists='append'
):
    pandas_df.to_sql(
        name=table_name, con=engine, schema=schema, index=index, if_exists=if_exists
    )
    delete_table(table_name, schema, engine)


def get_tables(schema, engine):
    insp = inspect(engine)
    return insp.get_table_names(schema)


def drop_table(table, schema, engine, close_connection=True):
    conn = engine.connect()
    conn.execute(f'DROP TABLE IF EXISTS {schema}.{table};')
    if close_connection:
        conn.close()


def delete_table(table_name, schema, engine, close_connection=True):
    conn = engine.connect()
    conn.execute(f'DELETE FROM {schema}.{table_name}')
    if close_connection:
        conn.close()


# ! Schema


def get_schemas(engine):
    insp = inspect(engine)
    return insp.get_schema_names()


def create_schema(schema_name, engine):
    if not engine.dialect.has_schema(engine, schema_name):
        engine.execute(sa.schema.CreateSchema(schema_name))
    else:
        return 'Already exists'


def drop_schema(schema, engine, close_connection=True):
    conn = engine.connect()
    conn.execute(f'DROP SCHEMA {schema}')
    if close_connection:
        conn.close()


# ! delete all tables from a schema
def apply_delete_to_schema(schema, engine, close_connection=True):
    conn = engine.connect()
    tables = get_tables(schema, engine)
    for i in tables:
        delete_table(i, schema, engine)
    if close_connection:
        conn.close()
