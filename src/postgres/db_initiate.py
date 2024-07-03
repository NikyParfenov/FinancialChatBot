import os
from glob import glob
from loguru import logger
from src.postgres.db_engine import create_tables, insert_vector_data, vectordb_data_amount, is_vectordb_empty
from src.engine.vectorization import vectorize_txt_file


def prepare_rds(dir='company_reports'):
    create_tables()
    if is_vectordb_empty():
        logger.info(f"Vector database is empty, trying to fill it from the local data {dir}...")
        for path in glob(os.path.join('src', dir, '*.txt')):
            with open(path, 'r') as file:
                data = file.read()
                company_name = os.path.split(file.name)[-1].split(".")[0]
            processed_data, _ = vectorize_txt_file(data, company_name)
            insert_vector_data(processed_data)
        logger.info(f"Vector database filling has been finished.")
    data_amount = vectordb_data_amount()
    logger.info(f"Vector database rows: {data_amount}")
        