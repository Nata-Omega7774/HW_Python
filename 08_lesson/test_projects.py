import pytest
import requests
import json
from config import API_TOKEN

BASE_URL = "https://yougile.com/api-v2"


class TestProjectsAPI:
    """Тесты для методов работы с проектами Yougile"""

    @pytest.fixture
    def auth_headers(self):
        return {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        }

    def create_temp_project(self, auth_headers, title="Test Project"):
        """Создание временного проекта"""
        data = {"title": title}

        response = requests.post(
            f"{BASE_URL}/projects",
            headers=auth_headers,
            json=data,
            timeout=10
        )

        print(f"Create project response: {response.status_code}, {response.text}")

        if response.status_code == 201:
            return response.json().get("id")
        return None

    def delete_project(self, auth_headers, project_id):
        """Удаление проекта"""
        try:
            response = requests.delete(
                f"{BASE_URL}/projects/{project_id}",
                headers=auth_headers,
                timeout=10
            )
            print(f"Delete project response: {response.status_code}")
        except requests.exceptions.RequestException:
            pass

    def test_check_auth(self, auth_headers):
        """Тест проверки авторизации"""
        response = requests.get(
            f"{BASE_URL}/projects",
            headers=auth_headers,
            timeout=10
        )
        print(f"Auth check response: {response.status_code}")

        if response.status_code == 401:
            pytest.skip("Неверный API токен. Пожалуйста, укажите правильный токен в config.py")

    def test_create_project_positive(self, auth_headers):
        """Позитивный тест создания проекта"""
        # Проверяем авторизацию
        auth_check = requests.get(f"{BASE_URL}/projects", headers=auth_headers)
        if auth_check.status_code == 401:
            pytest.skip("Неверный API токен")

        data = {"title": "New Test Project"}

        response = requests.post(
            f"{BASE_URL}/projects",
            headers=auth_headers,
            json=data,
            timeout=10
        )

        print(f"Create positive response: {response.status_code}, {response.text}")

        assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.text}"

        # Проверяем структуру ответа
        response_data = response.json()
        print(f"Response data: {response_data}")

        # Проверяем разные возможные форматы ответа
        if "title" in response_data:
            assert response_data["title"] == data["title"]
        elif "name" in response_data:
            assert response_data["name"] == data["title"]

        assert "id" in response_data

        # Очистка
        project_id = response_data["id"]
        self.delete_project(auth_headers, project_id)

    def test_create_project_negative_no_title(self, auth_headers):
        """Негативный тест - создание проекта без названия"""
        auth_check = requests.get(f"{BASE_URL}/projects", headers=auth_headers)
        if auth_check.status_code == 401:
            pytest.skip("Неверный API токен")

        data = {}  # Пустой объект без title

        response = requests.post(
            f"{BASE_URL}/projects",
            headers=auth_headers,
            json=data,
            timeout=10
        )

        print(f"Create negative response: {response.status_code}, {response.text}")
        assert response.status_code in [400,
                                        422], f"Expected 400 or 422, got {response.status_code}. Response: {response.text}"

    def test_get_project_positive(self, auth_headers):
        """Позитивный тест получения проекта"""
        auth_check = requests.get(f"{BASE_URL}/projects", headers=auth_headers)
        if auth_check.status_code == 401:
            pytest.skip("Неверный API токен")

        # Создаем временный проект
        project_id = self.create_temp_project(auth_headers, "Project to Get")
        if not project_id:
            pytest.skip("Не удалось создать проект для теста")

        try:
            # Получаем проект
            response = requests.get(
                f"{BASE_URL}/projects/{project_id}",
                headers=auth_headers,
                timeout=10
            )

            print(f"Get project response: {response.status_code}, {response.text}")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

            response_data = response.json()
            assert response_data["id"] == project_id

        finally:
            # Всегда удаляем проект
            self.delete_project(auth_headers, project_id)

    def test_get_project_negative_not_found(self, auth_headers):
        """Негативный тест - получение несуществующего проекта"""
        auth_check = requests.get(f"{BASE_URL}/projects", headers=auth_headers)
        if auth_check.status_code == 401:
            pytest.skip("Неверный API токен")

        response = requests.get(
            f"{BASE_URL}/projects/nonexistent_id_12345",
            headers=auth_headers,
            timeout=10
        )

        print(f"Get not found response: {response.status_code}, {response.text}")
        assert response.status_code == 404, f"Expected 404, got {response.status_code}. Response: {response.text}"

    def test_update_project_positive(self, auth_headers):
        """Позитивный тест обновления проекта"""
        auth_check = requests.get(f"{BASE_URL}/projects", headers=auth_headers)
        if auth_check.status_code == 401:
            pytest.skip("Неверный API токен")

        # Создаем временный проект
        project_id = self.create_temp_project(auth_headers, "Project to Update")
        if not project_id:
            pytest.skip("Не удалось создать проект для теста")

        try:
            # Обновляем проект (только title)
            update_data = {"title": "Updated Project Title"}

            response = requests.put(
                f"{BASE_URL}/projects/{project_id}",
                headers=auth_headers,
                json=update_data,
                timeout=10
            )

            print(f"Update project response: {response.status_code}, {response.text}")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

            response_data = response.json()
            print(f"Update response data: {response_data}")

            # Проверяем разные возможные форматы ответа
            if "title" in response_data:
                assert response_data["title"] == update_data["title"]
            elif "name" in response_data:
                assert response_data["name"] == update_data["title"]

        finally:
            # Всегда удаляем проект
            self.delete_project(auth_headers, project_id)

    def test_update_project_negative_invalid_data(self, auth_headers):
        """Негативный тест - обновление с невалидными данными"""
        auth_check = requests.get(f"{BASE_URL}/projects", headers=auth_headers)
        if auth_check.status_code == 401:
            pytest.skip("Неверный API токен")

        # Создаем временный проект
        project_id = self.create_temp_project(auth_headers, "Project for Invalid Update")
        if not project_id:
            pytest.skip("Не удалось создать проект для теста")

        try:
            # Пытаемся обновить с пустым названием
            invalid_data = {"title": ""}

            response = requests.put(
                f"{BASE_URL}/projects/{project_id}",
                headers=auth_headers,
                json=invalid_data,
                timeout=10
            )

            print(f"Update invalid response: {response.status_code}, {response.text}")
            assert response.status_code in [400,
                                            422], f"Expected 400 or 422, got {response.status_code}. Response: {response.text}"

        finally:
            # Всегда удаляем проект
            self.delete_project(auth_headers, project_id)
