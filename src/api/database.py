import psycopg2
import dotenv
import os
from contextlib import contextmanager
from src.api.core import Tg

dotenv.load_dotenv()


@contextmanager
def get_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST')
    )
    try:
        yield conn
    finally:
        conn.close()


def execute_db_query(query, parameters, fetch_one=False):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        if fetch_one:
            return cursor.fetchone()
        conn.commit()


def fetch_session(session_name: str):
    query = "SELECT api_id, api_hash, session_name, phone, sms_code, sms_hash, secret_password FROM sessions WHERE session_name=%s"
    row = execute_db_query(query, (session_name,), fetch_one=True)
    if not row:
        return None
    return Tg(*row)


def update_session(tg: Tg):
    print(tg)
    query = "UPDATE sessions SET api_id=%s, api_hash=%s, phone=%s, sms_code=%s, sms_hash=%s, secret_password=%s WHERE session_name=%s"
    execute_db_query(query,
                     (tg.api_id, tg.api_hash, tg.phone, tg.sms_code, tg.sms_hash, tg.secret_password, tg.session_name))


def create_session(tg: Tg):
    query = "INSERT INTO sessions (api_id, api_hash, phone, sms_hash, session_name) VALUES (%s, %s, %s, %s, %s);"
    execute_db_query(query, (tg.api_id, tg.api_hash, tg.phone, tg.sms_hash, tg.session_name))


def create_call(call_id, session_name):
    query = "INSERT INTO notifications (call_id, session_name) VALUES (%s, %s);"
    execute_db_query(query, (call_id, session_name))


def is_call_exists(call_id, session_name):
    query = "SELECT * FROM notifications WHERE session_name=%s AND call_id=%s;"
    row = execute_db_query(query, (session_name, call_id), fetch_one=True)
    return row is not None


# Есть звонок появился - создаем его
# Если звонок существует - говорим что он есть и уведомление не нужно
# Если звонок завершился - удаляем его по call_Id

def save_tg_entity(tg):
    session = fetch_session(tg.session_name)
    if not session:
        create_session(tg)
    else:
        update_session(tg)


def get_tg_entity(session_name: str):
    return fetch_session(session_name)
