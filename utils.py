import psycopg2
from config import config
from hh_api import HHParser


def create_database(name_db: str):
    """Функция создания базы данных"""
    params = config()
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {name_db}")
    cur.execute(f"CREATE DATABASE {name_db}")

    cur.close()
    conn.close()


def create_tables(name_db: str):
    """Функция создания таблиц в базе данных"""
    params = config()
    conn = psycopg2.connect(dbname=name_db, **params)
    with conn:
        with conn.cursor() as cur:
            cur.execute(""
                        "CREATE TABLE employers ("
                        "id int PRIMARY KEY, "
                        "name varchar(255) NOT NULL)");

            cur.execute(""
                        "CREATE TABLE vacancies ("
                        "id int PRIMARY KEY, "
                        "name varchar(255) NOT NULL, "
                        "area varchar(255), "
                        "url varchar(255), "
                        "salary_from int, "
                        "salary_to int, "
                        "employer_id int REFERENCES employers(id) NOT NULL)")
    conn.close()


def insert_tables(name_db):
    hh_parser = HHParser()
    employers = hh_parser.get_employers()
    vacancies = hh_parser.get_all_vacancies_by_employers()
    params = config()
    conn = psycopg2.connect(dbname=name_db, **params)
    with conn:
        with conn.cursor() as cur:
            for employer in employers:
                cur.execute("INSERT INTO employers VALUES (%s, %s)",
                            (employer['id'], employer['name']))
            for vacancy in vacancies:
                cur.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (vacancy['id'], vacancy['name'], vacancy['area'], vacancy['url'],
                             vacancy['salary_from'], vacancy['salary_to'], vacancy['employer_id']))
    conn.close()
