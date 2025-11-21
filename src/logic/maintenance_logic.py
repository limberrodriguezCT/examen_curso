from src.database.db import get_connection
import sqlite3

class MaintenanceLogic:
    @staticmethod
    def create_log(vehicle_id, description, cost):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO maintenance_logs (vehicle_id, description, cost, log_date)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """, (vehicle_id, description, cost))
            conn.commit()
            return True, "Mantenimiento registrado."
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def read_all():
        conn = get_connection()
        cursor = conn.cursor()
        # Usamos LEFT JOIN por seguridad visual
        query = """
            SELECT m.id, v.plate_number, v.model, m.description, m.cost, m.log_date, m.vehicle_id
            FROM maintenance_logs m
            LEFT JOIN vehicles v ON m.vehicle_id = v.id
            ORDER BY m.log_date DESC
        """
        data = cursor.fetchall()
        conn.close()
        return data

    # --- NUEVAS FUNCIONES PARA COMPLETAR EL CRUD ---
    @staticmethod
    def update(log_id, description, cost):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE maintenance_logs 
                SET description=?, cost=?
                WHERE id=?
            """, (description, cost, log_id))
            conn.commit()
            return True, "Registro actualizado."
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def delete(log_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM maintenance_logs WHERE id=?", (log_id,))
            conn.commit()
            return True, "Registro eliminado."
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()