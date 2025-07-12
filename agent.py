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
        stmt = insert(table).values(**row) # standard SQL statement expressed programmatically
        with engine.begin() as connection:
            connection.execute(stmt)
            

table_name = "receipts"
receipts = Table(
    table_name,
    metadata_obj,
    Column("receipt_id", Integer, primary_key=True),
    Column("customer_name", String(16), primary_key=True),
    Column("price", Float),
    Column("tip", Float),
)    