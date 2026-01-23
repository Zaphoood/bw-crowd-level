from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()


def db_url_from_env() -> str:
    user = os.environ["DB_USER"]
    password = os.environ["DB_PASSWORD"]
    host = os.environ["DB_HOST"]
    port = os.environ["DB_PORT"]
    name = os.environ["DB_NAME"]

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"


engine = create_engine(db_url_from_env())
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
