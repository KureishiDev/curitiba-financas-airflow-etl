import os
from sqlalchemy import create_engine


DEFAULT_DB_URI = "postgresql+psycopg2://postgres:vini@localhost:5432/curitiba_financas"

def get_engine():
    db_uri = os.getenv("CURITIBA_DB_URI", DEFAULT_DB_URI)
    return create_engine(db_uri)
