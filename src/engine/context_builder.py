import os
from datetime import datetime
from loguru import logger


def assistant_context(use_case, **kwargs) -> str:
    
    match use_case:
        case 'dialog':
            with open(os.path.join('src', 'llm_prompts', 'dialog.txt'), 'r') as file:
                instructions = file.read()
            companies = '[]' if 'companies' not in kwargs else str(kwargs['companies'])
            financial_information = '[]' if 'docs_content' not in kwargs else str(kwargs['docs_content'])
            system_prompt = instructions.format(date=str(datetime.now().date()), companies=companies, financial_information=financial_information)
        
        case 'intent':
            with open(os.path.join('src', 'llm_prompts', 'intent.txt'), 'r') as file:
                instructions = file.read()
            system_prompt = instructions.format(date=str(datetime.now().date()))

        case _:
            raise ValueError('invalid action')
        
    logger.info(f"Building LLM system instructions for '{use_case}' case.")
    return system_prompt