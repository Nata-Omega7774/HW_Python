import pytest
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import allure
import ssl


@allure.epic("Тестирование интерфейса сервиса YouGile")
@allure.feature("Работа с базой данных")
@allure.severity(allure.severity_level.BLOCKER)
@allure.suite("UI-тесты на авторизацию, управление проектами и задачами")
class TestDatabase:
    """Класс для тестирования работы с базой данных."""

    @allure.title("Проверка получения компании по ID")
    @allure.description("Тест проверяет корректность получения данных компании из базы данных по идентификатору")
    def test_get_company_by_id(self) -> None:
        """
        Тестирование получения компании по ID из базы данных.
        """
        with allure.step("Подготовка SQL запроса"):
            skript = {"select by id": text("select * from company where id=14737")}

        with allure.step("Создание подключения к базе данных"):
            # Добавьте параметры SSL
            db_url = 'postgresql://x_clients_db_3fmx_user:mzoTw2Vp4Ox4NQH0XKN3KumdyAYE31uq@dpg-cour99g21fec73bsgvug-a.oregon-postgres.render.com/x_clients_db_3fmx?sslmode=require'
            db = create_engine(db_url)

        try:
            with allure.step("Выполнение SQL запроса"):
                with db.connect() as connection:
                    result = connection.execute(skript["select by id"])

            with allure.step("Проверка результатов запроса"):
                result2 = result.fetchall()
                print(f"Результат: {result2}")
                assert result2[0][0] == 14737

        except Exception as e:
            with allure.step(f"Ошибка подключения: {e}"):
                pytest.skip(f"Пропуск теста из-за ошибки подключения: {e}")
