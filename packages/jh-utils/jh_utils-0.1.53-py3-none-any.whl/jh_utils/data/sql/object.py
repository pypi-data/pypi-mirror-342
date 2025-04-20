from jh_utils.data.sql.connection import create_connection, create_string_connection
from jh_utils.data.sql.manipulate_db import (
    get_tables,
    drop_table,
    delete_table,
    get_schemas,
    create_schema,
    drop_schema,
)
from dotenv import dotenv_values
from sqlalchemy import inspect

doc = """
    env: db, user, pass, host, port
    ----------------------------
    example .env
    host=weather
    host1=weather
    db=weather
    user=weather
    pass=weather12
    port=5400
    schema=raw
    """


class DB:
    __doc__ = doc

    def __init__(self, db, user, password, host, port):
        self.db = db
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def engine(self):
        return create_connection(
            database=self.db,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )

    def uri(self):
        return create_string_connection(
            database=self.db,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )

    def __repr__(self) -> str:
        return f"""host: {self.host}\ndb:{self.db}"""

    # ! table
    def drop_table(self, table, schema):
        return drop_table(table, schema=schema, engine=self.engine())

    def delete_table(self, table_name, schema):
        delete_table(table_name, schema, self.engine(), close_connection=True)

    def get_schemas(self):
        return get_schemas(self.engine())

    def get_tables(self, schema):
        return get_tables(schema, self.engine())

    # ! schema
    def drop_schema(self, schema):
        drop_schema(schema=schema, engine=self.engine())

    def create_schema(self, schema_nema):
        create_schema(schema_nema, self.engine())

    def run_sql(self, sql):
        conn = self.engine().connect()
        conn.execute(sql)


##
# ? Second form to create the object
##


def create_object_DB(env_dict):
    __docstring__ = doc
    db_object = DB(
        db=env_dict['db'],
        user=env_dict['user'],
        password=env_dict['pass'],
        host=env_dict['host'],
        port=env_dict['port'],
    )
    return db_object


def create_object_DB_by_envfile(path='.env'):
    __docstring__ = doc
    env = dotenv_values(path)
    db_obect_created = create_object_DB(env)
    return db_obect_created
