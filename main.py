from db_manager import DBManager
from utils import create_database, create_tables, insert_tables

def main():
    """Основная логика, позволяет проверить все методы работы с БД"""
    name_db = "test5"
    create_database(name_db)
    create_tables(name_db)
    insert_tables(name_db)

    db_manager = DBManager(name_db)
    print("Привет. Ты можешь поработать с базой данных")
    print("Давай расскажу как...")
    answer1 = input("Хочешь посмотреть список всех компаний и \n"
                    "количество вакансий у каждой компании в базе данных,\n"
                    "введи да или нет\n")
    if answer1.lower() == 'да':
        result = db_manager.get_companies_and_vacancies_count()
        for elem in result:
            print(f"У компании {elem[0]} в базу внесено {elem[1]} вакансий")
    else:
        print("идем дальше...")

    answer2 = input("Хочешь посмотреть список всех вакансий в базе данных\n"
                    "введи да или нет\n")
    if answer2.lower() == 'да':
        result = db_manager.get_all_vacancies()
        for elem in result:
            print(f"В компании {elem[0]} открыта вакансия {elem[1]} \n"
                  f"предлагают зарплату от {elem[2]} до {elem[3]}\n"
                  f"вот ссылка на вакансию {elem[4]}\n"
                  f"----------------------------------")
    else:
        print("идем дальше...")

    answer3 = input("Хочешь посмотреть средние значения нижней и верхней границы зарплат\n"
                    "введи да или нет\n")
    if answer3.lower() == 'да':
        result = db_manager.get_avg_salary()
        res_1 = round(result[0][0], 2)
        res_2 = round(result[0][1], 2)
        print(f"Среднее значение нижней границы {res_1}")
        print(f"Среднее значение верхней границы {res_2}")
    else:
        print("идем дальше...")

    answer4 = input("Теперь логично посмотреть список тех вакансий, \n"
                    "у которых зарплата выше среднего порога \n"
                    "введи да или нет\n")
    if answer4.lower() == 'да':
        result = db_manager.get_vacancies_with_higher_salary()
        for elem in result:
            print(f"Открыта вакансия {elem[0]} с зарплатой от {elem[1]} до {elem[2]}\n"
                  f"вот ссылка на вакансию {elem[3]}\n"
                  f"----------------------------------")
    else:
        print("идем дальше...")

    answer5 = input("Теперь ты можешь посмотреть список тех вакансий, \n"
                    "в названии которых содержатся переданные тобою в метод слова, по умолчанию специалист\n"
                    "введи свои слова для запроса через пробел\n").split()
    result = db_manager.get_vacancies_with_keyword(answer5)
    if result:
        for elem in result:
            print(f"Открыта вакансия {elem[1]} в городе {elem[2]} с зарплатой от {elem[4]} до {elem[5]}\n"
                  f"вот ссылка на вакансию {elem[3]}\n"
                  f"----------------------------------")
    else:
        print("По запросу не найдено ни одной вакансии")

if __name__ == "__main__":
    main()