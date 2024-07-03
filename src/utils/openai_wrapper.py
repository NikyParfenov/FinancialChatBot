import functools
import time
import openai
from loguru import logger

def wrap_exception(func, retry_time=3, max_retry=3):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        for retry in range(1, max_retry + 1):
            try:
                return func(*args, **kwargs)
            except openai.RateLimitError as e:
                logger.warning(f"Rate limit exceeded. Retrying {retry} in {retry_time} seconds...")
                time.sleep(retry_time)
                error = e
            except (openai.APIError, openai.OpenAIError, openai.APIConnectionError, openai.APITimeoutError) as e:
                logger.warning(f"API error occurred. Retrying {retry} in {retry_time} seconds...")
                time.sleep(retry_time)
                error = e
            except openai.InternalServerError as e:
                logger.warning(f"Server error occurred. Retrying {retry} in {retry_time} seconds...")
                time.sleep(retry_time)
                error = e
            except OSError as e:
                logger.warning(f"Connection error occurred: {e}. Retrying {retry} in {retry_time} seconds...")
                time.sleep(retry_time)
                error = e
            except RuntimeError as e:
                logger.warning(f"Service error occurred: {e}. Retrying {retry} in {retry_time} seconds...")
                time.sleep(retry_time)
                error = e
        raise error
    return wrapped
