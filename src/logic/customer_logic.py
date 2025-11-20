from src.database.db import get_connection
import sqlite3

class CustomerLogic:
    @staticmethod
    def create(fullname, doc_number, gender, phone, address):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO customers (full_name, document_number, gender, number_telephone, address)
                VALUES (?, ?, ?, ?, ?)
            """, (fullname, doc_number, gender, phone, address))
            conn.commit()
            return True, "Cliente registrado con éxito"
        except sqlite3.IntegrityError:
            return False, "El número de documento ya existe."
        except Exception as e:
            return False, f"Error desconocido: {e}"
        finally:
            conn.close()

    @staticmethod
    def read_all():
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers ORDER BY id DESC")
            return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def update(id_customer, fullname, doc_number, gender, phone, address):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE customers 
                SET full_name=?, document_number=?, gender=?, number_telephone=?, address=?
                WHERE id=?
            """, (fullname, doc_number, gender, phone, address, id_customer))
            conn.commit()
            return True, "Cliente actualizado correctamente"
        except Exception as e:
            return False, f"Error al actualizar: {e}"
        finally:
            conn.close()

    @staticmethod
    def delete(id_customer):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customers WHERE id=?", (id_customer,))
            conn.commit()
            return True, "Cliente eliminado"
        except sqlite3.IntegrityError:
            return False, "No se puede eliminar: El cliente tiene rentas asociadas."
        finally:
            conn.close()