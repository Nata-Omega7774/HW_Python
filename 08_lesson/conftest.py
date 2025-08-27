import pytest
import requests
from config import API_TOKEN  # Импортируем токен из config

BASE_URL = "https://yougile.com/api-v2"


@pytest.fixture
def auth_headers():
    """Фикстура для авторизационных заголовков"""
    return {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
