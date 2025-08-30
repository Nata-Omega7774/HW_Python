# EmployeeApi.py
import requests


class EmployeeApi:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None

    def get_list_employee(self, params=None):
        response = requests.get(f"{self.base_url}/employee", params=params)
        return response.json()

    def get_employee_by_id(self, employee_id):
        response = requests.get(f"{self.base_url}/employee/{employee_id}")
        return response.json()

    def get_employee_by_id_without_id(self):
        response = requests.get(f"{self.base_url}/employee/")
        return response.json()

    def create_employee_without_auth_token(self, company_id, data):
        response = requests.post(f"{self.base_url}/employee", json=data)
        return response.json()

    def create_employee_without_body(self):
        response = requests.post(f"{self.base_url}/employee", json={})
        return response.json()

    def change_info_employee_without_auth_token(self, employee_id, data):
        response = requests.patch(f"{self.base_url}/employee/{employee_id}", json=data)
        return response.json()

    def change_info_employee_without_id(self, data):
        response = requests.patch(f"{self.base_url}/employee/", json=data)
        return response.json()

    def change_info_employee_without_body(self, employee_id):
        response = requests.patch(f"{self.base_url}/employee/{employee_id}", json={})
        return response.json()

    def change_info_employee_wrong_id(self, wrong_emp_id):
        response = requests.patch(f"{self.base_url}/employee/{wrong_emp_id}", json={})
        return response.json()