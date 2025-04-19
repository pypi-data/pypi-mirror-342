import sqlalchemy as sa
import psycopg2


def create_string(user, password, host, db, port, sgbd="postgresql"):
    connection_string = sa.engine.URL.create(
        drivername=sgbd,
        username=user,
        password=password,
        host=host,
        database=db,
        port=port)
    return connection_string


def create_connection(database: str, user: str, password: str, host: str, port: str, sgbd='postgresql'):
    """
    create_connection(database=env['db'], 
                  user=env['user'],
                  password=env['pass'], 
                  host=env['host'],
                  port=env['port'])

    """
    con_string = create_string_connection(
        database, user, password, host, port, sgbd='postgresql')
    # Creating db string connection
    return sa.create_engine(con_string)


def create_string_connection(database: str, user: str, password: str, host: str, port: str, sgbd='postgresql'):
    """
    create_string_connection(database=env['db'], 
                  user=env['user'],
                  password=env['pass'], 
                  host=env['host'],
                  port=env['port'])
    """

    # Creating db string connection
    if sgbd == 'postgresql':
        con_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    if sgbd == 'mysql':
        con_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
    if sgbd == 'redshift':
        con_string = f'redshift+psycopg2://{user}:{password}@{host}:{port}/{database}'
    return con_string
