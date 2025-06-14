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

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        return self.execute_query(
            "SELECT employer_name, COUNT(vacancy_id) as count_vacancies "
            "FROM employers JOIN vacancies USING(employer_id) GROUP BY employer_id")

    def get_all_vacancies(self):
        """Получает список всех вакансий"""
        return self.execute_query(
            "SELECT employer_name, vacancy_name, salary_from, salary_to, url "
            "FROM employers JOIN vacancies USING(employer_id)")


    def get_avg_salary(self):
        """Получает средний порог зарплат по вакансиям"""
        return self.execute_query(
            "SELECT avg(salary_from) as avg_salary_from, avg(salary_to) as avg_salary_to FROM vacancies")

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше среднего порога"""
        return self.execute_query(
            "SELECT vacancy_name, salary_from, salary_to, url FROM vacancies "
            "where salary_from>(SELECT avg(salary_from) FROM vacancies) AND "
            "salary_to>(SELECT avg(salary_to) FROM vacancies)")


    def get_vacancies_with_keyword(self, keyword_list=['специалист']):
        """Получает список всех вакансий, в названии которых содержатся переданные
        в метод слова, по умолчанию специалист"""
        filtered_vacancies = []
        for word in keyword_list:
            vacancies = self.execute_query(
                f"SELECT * FROM vacancies where vacancy_name ILIKE '%{word}%'")
            for vacancy in vacancies:
                if vacancy not in filtered_vacancies:
                    filtered_vacancies.append(vacancy)
        return filtered_vacancies





