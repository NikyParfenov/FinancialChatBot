from loguru import logger
from glob import glob
from tqdm import tqdm

from src.llm_models.openai_models import get_embedding


def vectorize_txt_file(data, company_name):
    processed_data = []
    max_chunk_len = 0
    data_list = data.split("\n\n")
    logger.info(f"Start processing company '{company_name}' with {len(data_list)} articles...")

    for article in tqdm(data_list):
        max_chunk_len = max(max_chunk_len, len(article))
        chunk = f"{company_name}. {article}"
        vector = get_embedding(text=chunk, model = "text-embedding-3-small")
        processed_data.append((company_name, article, vector))

    logger.info(f"Finished processing company '{company_name}' with {len(data_list)} articles. Max chunk size is {max_chunk_len} characters")
    return processed_data, len(data_list)


if __name__ == "__main__":
    processed_data = []
    for path in glob('src/company_reports/*.txt'):
        processed_data.extend(vectorize_txt_file(path))
    print(len(processed_data))
