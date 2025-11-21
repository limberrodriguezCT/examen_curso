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
        # JOIN para ver la placa y modelo del carro, no solo el ID
        query = """
            SELECT m.id, v.plate_number, v.model, m.description, m.cost, m.log_date
            FROM maintenance_logs m
            JOIN vehicles v ON m.vehicle_id = v.id
            ORDER BY m.log_date DESC
        """
        data = cursor.fetchall()
        conn.close()
        return data