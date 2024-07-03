import psycopg2
import os
import uuid
from loguru import logger


class DataBaseProcessing:
    def __init__(self):
        super().__init__()

    @staticmethod
    def __connector():
        con = psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'),
            port=os.environ.get('POSTGRES_PORT'),
            database=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
        )
        return con


    @staticmethod
    def db_check():
        con = DataBaseProcessing.__connector()
        cur = con.cursor()
        cur.execute("SELECT 1")
        con.close()


    def get_messages(self, chat_id):
        with self.__connector() as con:
            with con.cursor() as cur:
                query = "SELECT role, content FROM chat_messages WHERE chat_id=%s ORDER BY created_at ASC;"
                cur.execute(query, (chat_id,))
                data = cur.fetchall() 
        con.close()
        return [{"role": i[0], "content": i[1]} for i in data]
    

    def add_message(self, chat_id, role, message):
        with self.__connector() as con:
            with con.cursor() as cur:
                query = "INSERT INTO chat_messages (id, chat_id, role, content) VALUES (%(id)s, %(chat_id)s, %(role)s, %(message)s);"
                cur.execute(query, {"id": uuid.uuid4(), "chat_id": chat_id, "role": role, "message": message})
                con.commit() 
        con.close()
        return


    def get_companies(self):
        with self.__connector() as con:
            with con.cursor() as cur:
                query = "SELECT DISTINCT company_name FROM vectorstore WHERE is_deleted=False;"
                cur.execute(query)
                data = cur.fetchall() 
        con.close()
        return [i for item in data for i in item ]


    def get_topk(self, embedding, company_name=None, topk=36, threshold=0.4):
        company_filter = '' if company_name is None else "AND company_name = %(company_name)s "

        with self.__connector() as con:
            with con.cursor() as cur:
                query = """SELECT 
                                id,
                                company_name,
                                content,
                                1 - (embedding <=> %(emb)s) as similarity
                            FROM vectorstore 
                            WHERE is_deleted=FALSE AND (1 - (embedding <=> %(emb)s)) > %(threshold)s {SQLFILTER} 
                            ORDER BY embedding <=> %(emb)s LIMIT %(topk)s;""".format(SQLFILTER=company_filter)
                cur.execute(query, {'emb': str(embedding), 'topk': topk, 'company_name': company_name, 'threshold': threshold})
                data = cur.fetchall() 
        con.close()
        return data
    