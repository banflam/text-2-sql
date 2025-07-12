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

