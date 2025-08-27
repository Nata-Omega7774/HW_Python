import pytest
import requests
from Pages.Employee import Employer, Company

employer = Employer()
company = Company()

def test_authorization(get_token):
   token = get_token
   assert token is not None
   assert isinstance(token, str)

def test_getcompany_id():
   company_id = company.last_active_company_id()
   assert company_id is not None
   assert str(company_id).isdigit()

def test_add_employer(get_token):
   token = str(get_token)
   com_id = company.last_active_company_id()
   body_employer = {
      "id": 0,
      "firstName": "Natalya",
      "lastName": "Ivanova",
      "middleName": "string",
      "companyId": com_id,
      "email": "test@mail.ru",
      "url": "string",
      "phone": "string",
      "birthdate": "2024-07-20T08:34:03.693Z",
      "isActive": 'true'
      }
   new_employer_id = (employer.add_new(token, body_employer))['id']
   assert new_employer_id is not None
   assert str(new_employer_id).isdigit()

   info = employer.get_info(new_employer_id)
   assert info.json()['id'] == new_employer_id
   assert info.status_code == 200

def test_add_employer_without_token():
  com_id = company.last_active_company_id()
  token = ""
  body_employer = {
      "id": 0,
      "firstName": "Natalya",
      "lastName": "Ivanova",
      "middleName": "string",
      "companyId": com_id,
      "email": "test@mail.ru",
      "url": "string",
      "phone": "string",
      "birthdate": "2024-07-20T08:34:03.693Z",
      "isActive": 'true'
      }
  new_employer = employer.add_new(token, body_employer)
  assert new_employer['message'] == 'Unauthorized'

def test_add_employer_without_body(get_token):
   token = str(get_token)
   com_id = company.last_active_company_id()
   body_employer = {}
   new_employer = employer.add_new(token, body_employer)
   assert new_employer['message'] == 'Innternal server error'

def test_get_employer():
   com_id = company.last_active_company_id()
   list_employers = employer.get_list(com_id)
   assert isinstance(list_employers, list)

   # ОР: ключ - значение
   assert result_db[0][6] == result_api.get('middleName')
   assert result_db[0][11] == result_api.get('companyId')
   # assert result_db[0][9] == result_api.get('birthdate') # дата через запятую как исправить?