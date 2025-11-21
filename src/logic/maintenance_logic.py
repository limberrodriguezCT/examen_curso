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
            return True, "Mantenimiento registrado correctamente."
        except Exception as e:
            return False, f"Error BD: {e}"
        finally:
            conn.close()

    @staticmethod
    def read_all():
        conn = get_connection()
        cursor = conn.cursor()
        # CONSULTA ROBUSTA:  LEFT JOIN y COALESCE: Si se borró el vehículo, mostrará "Vehículo Eliminado" en vez de ocultar el registro
        query = """
            SELECT 
                m.id, 
                COALESCE(v.plate_number, '---') as placa, 
                COALESCE(v.model, 'Vehículo Eliminado') as modelo, 
                m.description, 
                m.cost, 
                m.log_date, 
                m.vehicle_id
            FROM maintenance_logs m
            LEFT JOIN vehicles v ON m.vehicle_id = v.id
            ORDER BY m.log_date DESC
        """
        try:
            cursor.execute(query)
            data = cursor.fetchall()
            print(f"[DEBUG MANTENIMIENTO] Se encontraron {len(data)} registros.")
            return data
        except Exception as e:
            print(f"[ERROR] Fallo consulta mantenimiento: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def update(log_id, description, cost):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE maintenance_logs SET description=?, cost=? WHERE id=?", (description, cost, log_id))
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