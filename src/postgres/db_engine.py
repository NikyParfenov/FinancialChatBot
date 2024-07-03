from tqdm import tqdm
from glob import glob
from typing import List, Tuple
from loguru import logger
import os

from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from src.postgres.db_models import Vectorstore
from src.postgres.db_models import Base


# engine = create_engine(f"postgresql+psycopg2://{os.environ.get('AWS_RDS_USERNAME')}:{os.environ.get('AWS_RDS_PASSWORD')}@{os.environ.get('AWS_RDS_ENDPOINT')}:{os.environ.get('AWS_RDS_PORT')}/{os.environ.get('AWS_RDS_DBNAME')}")
engine = create_engine(f"postgresql+psycopg2://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_HOST')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}")
SessionMaker = sessionmaker(bind=engine, expire_on_commit=False)


def create_tables():
    try:
        Base.metadata.create_all(engine)
        logger.info(f"Required components in DB - status [OK]")
    except Exception as e:
        logger.error(f"Required components in DB - status [ERROR]: {e}")


def is_vectordb_empty():
    with SessionMaker() as session:
        sql_query = session.query(Vectorstore).count()
    return sql_query == 0


def vectordb_data_amount():
    with SessionMaker() as session:
        data_amount = session.query(Vectorstore).filter(Vectorstore.is_deleted == False).count()
    return data_amount


def company_data_amount(company_name):
    with SessionMaker() as session:
        data_amount = session.query(Vectorstore).filter(Vectorstore.is_deleted == False, Vectorstore.company_name == company_name).count()
    return data_amount


def remove_vector_data(company_name):
     with SessionMaker() as session:
        session.query(Vectorstore).filter(Vectorstore.company_name == company_name).update({Vectorstore.is_deleted: True})
        session.commit()
     return


def insert_vector_data(data: List[Tuple[str, str, List[float]]]):
    session = SessionMaker()
    for item in tqdm(data):
        vector = Vectorstore()
        vector.company_name = item[0]
        vector.content = item[1]
        vector.embedding = item[2]
        session.add(vector)

    session.commit()
    session.close()

    logger.info(f"Data with vectors ({len(data)} chunks) successfully loaded to db")
    return
