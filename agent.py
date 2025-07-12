from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    Float,
    insert,
    inspect,
    text,
)

load_dotenv()

engine = create_engine("sqlite:///:memory")
metadata_obj = MetaData()

def insert_rows_into_table(rows, table, engine=engine):

    for row in rows:
        stmt = insert(table).values(**row)
        with engine.begin() as connection:
            connection.execute(stmt)
            

    