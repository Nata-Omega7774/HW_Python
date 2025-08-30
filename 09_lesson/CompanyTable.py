# CompanyTable.py
from sqlalchemy import create_engine, text

class CompanyTable:
    def __init__(self, connection_string):
        self.__db = create_engine(connection_string)
        self.__scripts = {
            "insert new": text("INSERT INTO company (\"name\") VALUES (:new_name) RETURNING id"),
            "get max id": text("SELECT MAX(id) FROM company"),
            "delete by id": text("DELETE FROM company WHERE id = :id_to_delete"),
            "get all": text("SELECT * FROM company ORDER BY id"),
            "get by id": text("SELECT * FROM company WHERE id = :id_to_get")
        }

    def create_company(self, name):
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["insert new"], {"new_name": name})
            conn.commit()
            return result.scalar()

    def get_max_id(self):
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["get max id"])
            return result.scalar()

    def delete_company(self, id):
        with self.__db.connect() as conn:
            conn.execute(self.__scripts["delete by id"], {"id_to_delete": id})
            conn.commit()

    def get_all(self):
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["get all"])
            return result.fetchall()

    def get_by_id(self, id):
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["get by id"], {"id_to_get": id})
            return result.fetchone()