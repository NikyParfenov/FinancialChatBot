from loguru import logger
from pydantic import BaseModel

from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from src.postgres.db_scripts import DataBaseProcessing
from src.postgres.db_initiate import prepare_rds
from src.postgres.db_engine import insert_vector_data, vectordb_data_amount, remove_vector_data, company_data_amount
from src.utils.logs_customize import logs_customize
from src.engine.vectorization import vectorize_txt_file
from src.engine.chat import run_assistant


class Message(BaseModel):
    chat_id: str
    message: str
    company: str | None = None



logs_customize()  # logger customisation
prepare_rds()  # create tables, fill initial data is db is empty

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthcheck")
async def root():
    DataBaseProcessing.db_check()
    return {"status": 200}


@app.get("/api/companies")
async def companies_list():
    try:
        db = DataBaseProcessing()
        return {"status": 200, "companies": db.get_companies()}
    
    except Exception as e:
        logger.error(f"Couldn't process user data due to the error: {e}")
        return {"status": 500, "error": e}


@app.post("/api/add_docs")
async def add_documents(file: UploadFile = File(...)):

    file_name = file.filename.rsplit(".", maxsplit=1)
    extension = file_name[1]

    if extension != "txt":
        raise HTTPException(status_code=415, detail=f"Unsupported file format [.{extension}], please use [.txt]")

    try:
        company_name = file_name[0]
        contents = file.file.read().decode("utf-8")

        processed_data, inserted_amount = vectorize_txt_file(data=contents, company_name=company_name)
        insert_vector_data(processed_data)
        data_amount = vectordb_data_amount()
        logger.info(f"Inserted data: {inserted_amount}; Vector database rows: {data_amount}")

        return {"status": 200, "inserted_data": inserted_amount, "total_amount": data_amount}
    
    except Exception as e:
        logger.error(f"Couldn't process user data due to the error: {e}")
        return {"status": 500, "error": e}


@app.post("/api/rm_docs")
async def chat_bot(company: Request):
    company_name = await company.json()
    company_name = company_name.get('company')
    comp_data_amount = company_data_amount(company_name)
    remove_vector_data(company_name)
    data_amount = vectordb_data_amount()
    logger.info(f"Company '{company_name}' with '{comp_data_amount}' rows has been deleted. Vector database rows: {data_amount}")
    return {"status": 200, "deleted_data": comp_data_amount, "total_amount": data_amount}


@app.post("/api/message")
async def chat_bot(request: Message):
    try:
        response = run_assistant(chat_id=request.chat_id, message=request.message, company_name=request.company)
    except Exception as e:
        logger.error(f"LLM error: {e}")
        response = "Sorry, something went wrong. Could you repeat your query?"

    return {"status": 200, "chat_id": request.chat_id, "response": response}
