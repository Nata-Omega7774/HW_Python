from sqlalchemy import create_engine, text

class EmployeeTable:
    def __init__(self, connection_string):
        self.__db = create_engine(connection_string)
        self.__scripts = {
            "insert new": text("INSERT INTO employee (company_id, is_active, first_name, last_name, middle_name, phone, email, birthdate, avatar_url) VALUES (:company_id, :is_active, :first_name, :last_name, :middle_name, :phone, :email, :birthdate, :avatar_url) RETURNING id"),
            "get list by company": text("SELECT * FROM employee WHERE company_id = :company_id ORDER BY id"),
            "get by id": text("SELECT * FROM employee WHERE id = :id"),
            "delete by company": text("DELETE FROM employee WHERE company_id = :company_id"),
            "update employee": text("UPDATE employee SET first_name = :first_name, last_name = :last_name, middle_name = :middle_name, phone = :phone, email = :email, birthdate = :birthdate, avatar_url = :avatar_url, is_active = :is_active WHERE id = :id")
        }

    def create_employee(self, company_id, is_active, employee_data):
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["insert new"], {
                "company_id": company_id,
                "is_active": is_active,
                "first_name": employee_data.get('first_name'),
                "last_name": employee_data.get('last_name'),
                "middle_name": employee_data.get('middle_name'),
                "phone": employee_data.get('phone'),
                "email": employee_data.get('email'),
                "birthdate": employee_data.get('birthdate'),
                "avatar_url": employee_data.get('url')
            })
            conn.commit()
            return result.scalar()

    def get_list_emps_by_id_company(self, company_id):
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["get list by company"], {"company_id": company_id})
            return result.fetchall()

    def get_emp_by_id(self, id):
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["get by id"], {"id": id})
            return result.fetchall()

    def delete_list_emps_by_company_id(self, company_id):
        with self.__db.connect() as conn:
            conn.execute(self.__scripts["delete by company"], {"company_id": company_id})
            conn.commit()

    def patch_employee(self, id, is_active, employee_data):
        with self.__db.connect() as conn:
            conn.execute(self.__scripts["update employee"], {
                "id": id,
                "is_active": is_active,
                "first_name": employee_data.get('first_name'),
                "last_name": employee_data.get('last_name'),
                "middle_name": employee_data.get('middle_name'),
                "phone": employee_data.get('phone'),
                "email": employee_data.get('email'),
                "birthdate": employee_data.get('birthdate'),
                "avatar_url": employee_data.get('url')
            })
            conn.commit()

    def get_list_id_emps_by_id_company(self, company_id):
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["get list by company"], {"company_id": company_id})
            return result.fetchall()