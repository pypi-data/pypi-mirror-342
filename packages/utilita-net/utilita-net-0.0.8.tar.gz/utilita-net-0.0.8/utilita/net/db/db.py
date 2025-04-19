from sqlalchemy.dialects import postgresql as pgcmd
import sqlalchemy as sa

def records_to_sql(records: iter, con: sa.engine, table: str, schema: str, upsert: bool=False, index_elements: list=None, chunksize=5000, upsert_missing_columns=True) -> bool:
    """ Inserts records into a table. Allows for upserts. This only works on postgresql for now.
    
    Params:
        records (iterator): a list of records in the form of [{col1=val1, col2=val2, col3=val3}]
        con (sqlalchemy engine): a sqlalchemy engine connection
        table (str): destination table name
        schema (str): destination schema name
        upsert (bool): whether to upsert the data. uses postgres dialect ON CONFLICT DO UPDATE
        index_elements (list): a list of column names to match the on conflict statement
        chunksize (int): chunk size to insert on
        upsert_missing_columns (bool): Default True, If True, a missing column will be set to null on upsert.

    Returns:
        True if import was successful
    
    """
    metadata = sa.MetaData()
    table_info = sa.Table(table, metadata, autoload_with=con, schema=schema)
    records = iter(records) # in case the iter is a list.

    if (index_elements is None or len(index_elements) == 0) and upsert:
        raise ValueError('No index_elements defined for the on conflict statement. You must define what columns the on conflict will hit.')

    with con.begin() as conn:
        has_more_data = True
        total_rows = 0
        while has_more_data:
            active_columns = set()
            records_to_insert = []

            for i in range(chunksize):
                try:
                    _ = next(records)
                    active_columns.update(_.keys())
                    records_to_insert.append(_)
                    total_rows += 1

                except StopIteration:
                    has_more_data = False
                    break

            if len(records_to_insert) > 0:
                insert_query = pgcmd.insert(table_info).values(records_to_insert)
                
                # Garbage collector is sometimes slow at removing this.
                del(records_to_insert)
                
                if upsert:
                        if not upsert_missing_columns:
                            try:
                                cols = {col: insert_query.excluded[col] for col in active_columns}
                            except KeyError as e:
                                 raise sa.exc.SQLAlchemyError(f'We are trying to update the column {e}, but it does not exist in {schema}.{table}')
                        else:
                             cols = {**insert_query.excluded}

                        insert_query = insert_query.on_conflict_do_update(
                        index_elements=index_elements,
                        set_=cols
                        )
                try:
                    conn.execute(insert_query)
                    print(f'Inserted {total_rows} rows' + (' so far..' if has_more_data else '.'))
                except sa.exc.SQLAlchemyError as e:
                    # Reraising the error will prevent potential errors that will take up MB of data from
                    #  a failed insert.
                    str_e = str(e)[:2000] + ' <<output truncated>>'
                    raise sa.exc.SQLAlchemyError('got sqlalchemy exception: ' + str_e) from None

    return True

def df_to_sql(df: object, *args, **kwargs):
    """ Wrapper function for records_to_sql(), however accepting a dataframe instead of a records iterator

        Params:
            df (pandas.DataFrame): a DataFrame object
            con (sqlalchemy engine): a sqlalchemy engine connection
            table (str): destination table name
            schema (str): destination schema name
            upsert (bool): upserts the data. uses postgres dialect ON CONFLICT DO UPDATE
            index_elements (list): a list of column names to match the on conflict statement
            chunksize (int): chunk size to insert on

        Returns:
            True if import was successful
    """
    try:
        import pandas as pd
        records = (row.to_dict() for index, row in df.iterrows())
        return records_to_sql(records=records, *args, **kwargs)
    except ImportError:
            raise ImportError('Pandas is not installed or could not be imported.')