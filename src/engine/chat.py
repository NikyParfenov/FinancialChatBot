import re
from loguru import logger
from src.engine.context_builder import assistant_context
from src.llm_models.openai_models import completion_block, get_embedding
from src.postgres.db_scripts import DataBaseProcessing


def intent_recognition(chat_history):
    
    intent_completion = 'None'
    user_question = None

    intent_context = [{"role": "system", "content":  assistant_context(use_case='intent')},
                      *chat_history[-2:]]

    intent_completion = completion_block(conversation=intent_context, model='gpt-4-turbo', temp=0.5, tokens=96)
    logger.info(f'Intent answer: {intent_completion}')

    user_intents_string = re.search(r'(intents:)(.*)[^\n]', intent_completion, flags=re.I)
    user_question_string = re.search(r'(question:)(.*)[^\n]', intent_completion, flags=re.I)

    if user_question_string:
        user_question_string = user_question_string.group()
        user_question = re.sub(r"[\([{})\]]", '', 
                                re.search(r'(?<=question: )[^\n]*', user_question_string, flags=re.I).group().replace("'", '').replace('"', '')
                                )

    if user_intents_string:
        user_intents_string = user_intents_string.group()
        user_intents = list(map(lambda x: x.replace("'", '').replace('"', ''),
                                re.sub(r"[\([{})\]]", '',
                                    re.search(r'(?<=intents: )[^\n]*', user_intents_string, flags=re.I).group()
                                    ).split(', ')
                                )
                            )
    else:
        user_intents = ['other']

    logger.info(f'User intent: {user_intents}')
    return user_intents, user_question


def llm_response(chat_history, companies, docs_content):
    dialog_context = [{"role": "system", "content":  assistant_context(use_case='dialog', companies=companies, docs_content=docs_content)},
                      *chat_history[-9:]]

    response = completion_block(conversation=dialog_context, model='gpt-4-turbo', temp=0.5, tokens=2048)
    logger.info(f'LLM answer: {response}')
    return response


def run_assistant(chat_id, message, company_name=None):

    if company_name in [None, 'None', 'null', '']:
        company_name = None
    else:
        message += '\n({company_name} company)'.format(company_name=company_name)

    db = DataBaseProcessing()
    db.add_message(chat_id=chat_id, role="user", message=message)
    chat_history = db.get_messages(chat_id=chat_id)
    logger.info(f'Chat ID: {chat_id}; History load: {len(chat_history)} messages')

    user_intents, user_question = intent_recognition(chat_history=chat_history)

    if any(item.strip() in ['bad_request'] for item in user_intents):
        response = "Sorry, but I'm here to assist you with questions about companies' financial reports. Could you please specify your question in this area?"
        return response

    if any(item.strip() in ['ask_question'] for item in user_intents):
        question = message if user_question is None else user_question
        query_emb = get_embedding(text=question, model = "text-embedding-3-small")
        topk_docs = db.get_topk(query_emb, company_name=company_name, topk=60, threshold=0.5)
        docs = "\n".join([f"{i[1]}: {i[2]}" for i in topk_docs])
        logger.info(f"Loaded data from vectorDB: {[(i[0], i[3]) for i in topk_docs]}")
    else:
        docs = '[]'
    
    response = llm_response(chat_history=chat_history, companies=db.get_companies(), docs_content=docs)
    db.add_message(chat_id=chat_id, role="assistant", message=str(response))
    return response
