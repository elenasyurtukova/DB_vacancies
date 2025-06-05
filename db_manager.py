from typing import Any

import psycopg2

from config import config

class DBManager:
    """Класс методов работы с данными в таблицах БД"""
    def __init__(self, db_name: str):
        """Метод инициализации класса"""
        self.__db_name = db_name


    def execute_query(self, query: str) -> Any:
        """Метод выполнения запроса в БД"""
        params = config()
        conn = psycopg2.connect(dbname=self.__db_name, **params)
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                res = cur.fetchall()
        conn.close()
        return res

    def get_all_employers(self):
        return self.execute_query("SELECT * FROM employers")