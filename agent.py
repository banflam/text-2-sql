from dotenv import load_dotenv
from smolagents import tool, CodeAgent, InferenceClientModel
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
    Column("customer_name", String(16)),
    Column("price", Float),
    Column("tip", Float),
)    

metadata_obj.create_all(engine)

rows = [
    {"receipt_id": 1, "customer_name": "Alan Payne", "price": 12.06, "tip": 1.20},
    {"receipt_id": 2, "customer_name": "Alex Mason", "price": 23.86, "tip": 0.24},
    {"receipt_id": 3, "customer_name": "Woodrow Wilson", "price": 53.43, "tip": 5.43},
    {"receipt_id": 4, "customer_name": "Margaret James", "price": 21.11, "tip": 1.00},
]

insert_rows_into_table(rows, receipts)

inspector = inspect(engine)
columns_info = [(col["name"], col["type"]) for col in inspector.get_columns("receipts")]
table_description = "Columns:\n" + "\n".join([f" - {name}: {col_type}" for name, col_type in columns_info])
print(table_description)

@tool
def sql_engine(query: str) -> str:
    """
    Allows you to perform SQL queries on the table. Returns a string representation of the result.
    The table name is "Receipts" and its description is as follows:

    Tables:

    Receipts:
    - receipt_id: INTEGER
    - customer_name: VARCHAR(16)
    - price: FLOAT
    - tip: FLOAT

    Waiters:
    - receipt_id: INTEGER (Foreign key to Receipts.receipt_id)
    - waiter_name: VARCHAR(16)

    Args:
        query: The query to perform. This must be correct SQL.
    """
    output = ""
    with engine.connect() as connection:
        rows = connection.execute(text(query))
        for row in rows:
            output += "\n" + str(row)
    return output

agent = CodeAgent(
    tools = [sql_engine],
    model = InferenceClientModel(model_id="meta-llama/Llama-3.1-8B-Instruct")
)

agent.run("Can you give me the receipt id of the most expensive receipt?")

table_name = "waiters"
waiters = Table(
    table_name,
    metadata_obj,
    Column("receipt_id", Integer, primary_key=True),
    Column("waiter_name", String(16)),
)

metadata_obj.create_all(engine)

rows = [
    {"receipt_id": 1, "waiter_name": "Corey Johnson"},
    {"receipt_id": 2, "waiter_name": "Michael Watts"},
    {"receipt_id": 3, "waiter_name": "Michael Watts"},
    {"receipt_id": 4, "waiter_name": "Margaret James"},
]

insert_rows_into_table(rows, waiters)

sql_join_capable_agent = CodeAgent(
    tools=[sql_engine],
    model = InferenceClientModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct"),
)

sql_join_capable_agent.run("Which waiter got more money from tips?")