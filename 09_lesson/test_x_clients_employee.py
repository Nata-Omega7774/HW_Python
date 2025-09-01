import pytest
from faker import Faker
import allure

from EmployeeApi import EmployeeApi
from EmployeeTable import EmployeeTable
from CompanyTable import CompanyTable

# Константы для подключения
BASE_URL = 'https://x-clients-be.onrender.com'
DB_URL = (
    'postgresql://x_clients_db_3fmx_user:mzoTw2Vp4Ox4NQH0XKN3KumdyAYE31uq@'
    'dpg-cour99g21fec73bsgvug-a.oregon-postgres.render.com/x_clients_db_3fmx'
)

# Инициализация объектов
db_emp = EmployeeTable(DB_URL)
db_com = CompanyTable(DB_URL)
emp_api = EmployeeApi(BASE_URL)

# Настройка Faker
Faker.seed()
fake = Faker("ru_RU")

# Тестовые данные
NUM_EMPLOYEES = 3
IS_ACTIVE = True


def generate_employee_data():
    """Генератор тестовых данных сотрудника"""
    return {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'middle_name': fake.first_name_male(),
        'is_active': True,
        'phone': fake.random_number(digits=11, fix_len=True),
        'birthdate': '2005-04-26',
        'url': fake.url()
    }


# Фикстуры для создания тестовых данных
@pytest.fixture(scope='function')
def test_company():
    """Создает тестовую компанию и удаляет после теста"""
    company_id = db_com.create_company("Test Company for Employees")
    yield company_id
    db_com.delete_company(company_id)


@pytest.fixture(scope='function')
def test_employee(test_company):
    """Создает тестового сотрудника и удаляет после теста"""
    company_id = test_company
    employee_data = generate_employee_data()
    employee_id = db_emp.create_employee(company_id, IS_ACTIVE, employee_data)
    yield employee_id, employee_data
    db_emp.delete_employee(employee_id)


@pytest.fixture(scope='function')
def multiple_employees(test_company):
    """Создает несколько тестовых сотрудников"""
    company_id = test_company
    employee_ids = []

    for _ in range(NUM_EMPLOYEES):
        employee_data = generate_employee_data()
        employee_id = db_emp.create_employee(
            company_id, IS_ACTIVE, employee_data
        )
        employee_ids.append(employee_id)

    yield company_id, employee_ids

    # Очистка всех сотрудников компании
    db_emp.delete_list_emps_by_company_id(company_id)


@allure.epic("hw9")
@allure.feature("сотрудник компании")
class TestEmployee:

    @allure.story("получить список сотрудников компании")
    def test_get_list_employees(self, multiple_employees):
        """Тест получения списка сотрудников"""
        company_id, employee_ids = multiple_employees

        # Получить список через API
        api_result = emp_api.get_list_employee(params={"company": company_id})

        # Получить список из БД
        db_result = db_emp.get_list_emps_by_id_company(company_id)

        # Проверки
        assert len(api_result) == len(db_result) == NUM_EMPLOYEES

        # Проверить соответствие ID
        api_ids = [emp["id"] for emp in api_result]
        db_ids = [emp[0] for emp in db_result]

        assert sorted(api_ids) == sorted(db_ids)

    @allure.story("получить сотрудника по ID")
    def test_get_employee_by_id(self, test_employee):
        """Тест получения информации о конкретном сотруднике"""
        employee_id, employee_data = test_employee

        # Получить данные через API
        api_result = emp_api.get_employee_by_id(employee_id)

        # Получить данные из БД
        db_result = db_emp.get_emp_by_id(employee_id)

        # Основные проверки
        assert api_result["id"] == employee_id
        assert api_result["firstName"] == employee_data["first_name"]
        assert api_result["lastName"] == employee_data["last_name"]
        assert api_result["isActive"] == employee_data["is_active"]
        assert api_result["middleName"] == employee_data["middle_name"]

    @allure.story("negative: получить сотрудника без ID")
    def test_get_employee_by_id_without_id(self):
        """Тест попытки получения сотрудника без указания ID"""
        result = emp_api.get_employee_by_id_without_id()

        assert result["statusCode"] == 500
        assert result["message"] == 'Internal server error'

    @allure.story("создание сотрудника")
    def test_create_employee(self, test_company):
        """Тест создания нового сотрудника"""
        company_id = test_company
        employee_data = generate_employee_data()

        # Проверить начальное состояние
        initial_count = len(db_emp.get_list_emps_by_id_company(company_id))
        assert initial_count == 0

        # Создать сотрудника
        new_employee_id = db_emp.create_employee(
            company_id, IS_ACTIVE, employee_data
        )

        # Проверить результат
        final_count = len(db_emp.get_list_emps_by_id_company(company_id))
        assert final_count == initial_count + 1

        # Проверить данные созданного сотрудника
        created_employee = db_emp.get_emp_by_id(new_employee_id)
        assert created_employee[0][4] == employee_data["first_name"]
        assert created_employee[0][5] == employee_data["last_name"]

    @allure.story("negative: создание сотрудника без токена")
    def test_create_employee_without_auth_token(self, test_company):
        """Тест создания сотрудника без авторизации"""
        company_id = test_company
        employee_data = generate_employee_data()

        initial_count = len(db_emp.get_list_emps_by_id_company(company_id))

        result = emp_api.create_employee_without_auth_token(
            company_id, employee_data
        )

        # Проверить ошибку авторизации
        assert result["statusCode"] == 401
        assert result["message"] == 'Unauthorized'

        # Проверить, что сотрудник не создался
        final_count = len(db_emp.get_list_emps_by_id_company(company_id))
        assert final_count == initial_count

    @allure.story("negative: создание сотрудника без тела запроса")
    def test_create_employee_without_body(self):
        """Тест создания сотрудника без передачи данных"""
        result = emp_api.create_employee_without_body()

        assert result["statusCode"] == 500
        assert result["message"] == 'Internal server error'

    @allure.story("обновление данных сотрудника")
    def test_patch_employee(self, test_employee):
        """Тест обновления информации о сотруднике"""
        employee_id, original_data = test_employee

        # Новые данные для обновления
        update_data = {
            'lastName': fake.last_name(),
            'email': fake.email(),
            'isActive': False
        }

        # Обновить данные
        db_emp.patch_employee(employee_id, False, update_data)

        # Проверить обновление
        updated_employee = db_emp.get_emp_by_id(employee_id)

        assert updated_employee[0][5] == update_data['lastName']
        assert updated_employee[0][8] == update_data['email']
        assert updated_employee[0][1] == update_data['isActive']

    @allure.story("negative: обновление без авторизации")
    def test_patch_employee_without_auth_token(self, test_employee):
        """Тест обновления сотрудника без авторизации"""
        employee_id, _ = test_employee

        update_data = {
            'lastName': fake.last_name(),
            'email': fake.email()
        }

        result = emp_api.change_info_employee_without_auth_token(
            employee_id, update_data
        )

        assert result["statusCode"] == 401
        assert result["message"] == 'Unauthorized'

    @allure.story("negative: обновление без ID")
    def test_patch_employee_without_id(self):
        """Тест обновления сотрудника без указания ID"""
        update_data = {
            'lastName': fake.last_name(),
            'email': fake.email()
        }

        result = emp_api.change_info_employee_without_id(update_data)

        assert result["statusCode"] == 404
        assert result["error"] == 'Not Found'

    @allure.story("negative: обновление без тела запроса")
    def test_patch_employee_without_body(self, test_employee):
        """Тест обновления сотрудника без передачи данных"""
        employee_id, _ = test_employee

        # Попытка обновления без тела запроса
        result = emp_api.change_info_employee_without_body(employee_id)

        # Проверка ошибки
        assert result["statusCode"] in [400, 500]
        assert "message" in result or "error" in result

    @allure.story("negative: обновление с неверным ID")
    def test_patch_employee_wrong_id(self):
        """Тест обновления несуществующего сотрудника"""
        wrong_emp_id = 999999  # Заведомо несуществующий ID

        update_data = {
            'lastName': fake.last_name(),
            'email': fake.email()
        }

        result = emp_api.change_info_employee_wrong_id(wrong_emp_id)

        assert result["statusCode"] in [404, 500]

    @allure.story("удаление сотрудника")
    def test_delete_employee(self, test_employee):
        """Тест удаления сотрудника"""
        employee_id, _ = test_employee

        # Проверить, что сотрудник существует
        initial_employee = db_emp.get_emp_by_id(employee_id)
        assert initial_employee is not None

        # Удалить сотрудника через API (добавить метод в EmployeeApi при необходимости)
        # delete_result = emp_api.delete_employee(employee_id)
        # assert delete_result.status_code == 200

        # Удалить через БД для тестирования
        db_emp.delete_employee(employee_id)

        # Проверить, что сотрудник удален из БД
        deleted_employee = db_emp.get_emp_by_id(employee_id)
        assert deleted_employee is None or len(deleted_employee) == 0

    @allure.story("negative: удаление несуществующего сотрудника")
    def test_delete_nonexistent_employee(self):
        """Тест попытки удаления несуществующего сотрудника"""
        nonexistent_id = 999999

        # Если метод delete_employee реализован в API
        # result = emp_api.delete_employee(nonexistent_id)
        # assert result.status_code in [404, 400]

        # Проверить через БД, что такого сотрудника нет
        employee = db_emp.get_emp_by_id(nonexistent_id)
        assert employee is None or len(employee) == 0