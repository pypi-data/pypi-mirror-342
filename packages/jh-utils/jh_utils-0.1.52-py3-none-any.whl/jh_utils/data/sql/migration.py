from jh_utils.data.pandas import sql
import dask.dataframe as dd


def migrate_table_pandas(query, table_name, engine_origin, engine_destiny, destiny_schema, if_exists):
    df = sql.get_sql_table(query, engine_origin)
    sql.write_table(df, table_name, destiny_schema, engine_destiny,
                    if_exists=if_exists, chunksize=10_000, index=False, close_connection=False)


def migrate_function_pandas(engine_origin,
                            engine_destiny,
                            destiny_schema,
                            index=False):
    def output_func(query, table_name, if_exists='replace', chunksize=10_000):
        df = sql.get_sql_table(query, engine_origin)
        sql.write_table(df, table_name, destiny_schema, engine_destiny,
                        if_exists=if_exists, chunksize=10_000,
                        index=False, close_connection=False)
    return output_func


def migrate_table_dask(table,
                       table_id,
                       input_schema,
                       output_schema,
                       uri_input,
                       uri_output,
                       npartitions,
                       bytes_per_chunk='256MB',
                       parallel=True,
                       if_exists='append',
                       method='multi'):
    df = dd.read_sql_table(table,
                           con=uri_input,
                           schema=input_schema,
                           index_col=table_id,
                           npartitions=npartitions,
                           bytes_per_chunk=bytes_per_chunk)
    # df = df.drop(f'{table_id}__1', axis=1)
    dd.to_sql(df,
              con=uri_output,
              name=table,
              schema=output_schema,
              if_exists=if_exists,
              parallel=parallel,
              method=method)


def send_to_s3bucket(file_name,
                     bucket_path,
                     table,
                     table_id,
                     input_schema,
                     uri_input,
                     npartitions,
                     bytes_per_chunk='256MB'):
    df = dd.read_sql_table(table=table,
                           uri=uri_input,
                           schema=input_schema,
                           index_col=table_id,
                           npartitions=npartitions,
                           bytes_per_chunk=bytes_per_chunk)
    # df = df.drop(f'{table_id}__1', axis=1)
    df.to_csv(bucket_path + file_name)


def migrate_function_dask(uri_input, uri_output):
    def output_func(table,
                    table_id,
                    input_schema,
                    output_schema,
                    npartitions,
                    bytes_per_chunk='256MB',
                    parallel=True,
                    if_exists='append',
                    method='multi'):
        df = dd.read_sql_table(table=table,
                               uri=uri_input,
                               schema=input_schema,
                               index_col=table_id,
                               npartitions=npartitions,
                               bytes_per_chunk=bytes_per_chunk)
        df = df.drop(f'{table_id}__1', axis=1)
        dd.to_sql(df,
                  uri=uri_output,
                  name=table,
                  schema=output_schema,
                  if_exists=if_exists,
                  parallel=parallel,
                  method=method)
    return output_func
