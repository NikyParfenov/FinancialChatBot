import os
from typing import Any, Dict, List
from loguru import logger
from openai import OpenAI
from src.utils.openai_wrapper import wrap_exception


@logger.catch
@wrap_exception
def completion_block(conversation: List[Dict[str, str]],
                     temp: float = 0.7,
                     model: str = "gpt-4-turbo", # 'gpt-4o'
                     tokens: int = 2048,
                     ) -> str:
    
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))  

    response = client.chat.completions.create(model=model,
                                              temperature=temp,
                                              max_tokens=tokens,
                                              messages=conversation)
    return response.choices[0].message.content


@logger.catch
@wrap_exception
def get_embedding(text: str,
                  model: str = "text-embedding-3-small",  # "text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"
                  ) -> List[float]:
    
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))  

    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding
