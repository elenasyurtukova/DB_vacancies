import requests


class HHParser:
    """Класс получения работодателей и вакансий с сайта hh.ru"""
    def __init__(self):
        """Метод инициализации класса"""
        self.__url_employers = "https://api.hh.ru/employers"
        self.__url_vacancies = "https://api.hh.ru/vacancies"


    def get_employers(self) -> list[dict]:
        """Метод получения списка работодателей"""
        params = {"sort_by": "by_vacancies_open", "per_page": 10}
        response = requests.get(self.__url_employers, params=params)
        response.raise_for_status()
        employers = response.json()["items"]
        return [{"employer_id": employer["id"], "employer_name": employer["name"]} for employer in employers]


    def get_vacancies_by_employer(self, employer_id: str) -> list[dict]:
        """Метод получения вакансий конкретного работодателя"""
        params = {"employer_id": employer_id, "per_page": 100}
        response = requests.get(self.__url_vacancies, params=params)
        response.raise_for_status()
        vacancies = response.json()["items"]
        return vacancies


    def get_all_vacancies_by_employers(self):
        employers = self.get_employers()
        all_vacancies = []
        for employer in employers:
            vacancies = self.get_vacancies_by_employer(employer["employer_id"])
            all_vacancies.extend([self.salary_for_vacancy(vacancy) for vacancy in vacancies])
        return all_vacancies


    @staticmethod
    def salary_for_vacancy(vacancy):
        """Метод получения минимальной и максимальной зарплаты для вакансии"""
        if vacancy["salary"]:
            salary_from = vacancy["salary"]["from"] if vacancy["salary"]["from"] else 0
            salary_to = vacancy["salary"]["to"] if vacancy["salary"]["to"] else 0
        else:
            salary_from = 0
            salary_to = 0
        return {"vacancy_id": vacancy["id"], "vacancy_name": vacancy["name"], "area": vacancy["area"]["name"],
                "url": vacancy["alternate_url"], "salary_from": salary_from, "salary_to": salary_to,
                "employer_id": vacancy["employer"]["id"]}


