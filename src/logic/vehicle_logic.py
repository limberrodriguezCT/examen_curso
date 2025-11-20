from src.database.db import get_connection
import sqlite3

class VehicleLogic:
    @staticmethod
    def create(model, plate, chassis, rate):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            # Por defecto is_available es 1 (Disponible)
            cursor.execute("""
                INSERT INTO vehicles (model, plate_number, chassis_number, daily_rate, is_available)
                VALUES (?, ?, ?, ?, 1)
            """, (model, plate, chassis, rate))
            conn.commit()
            return True, "Vehículo registrado con éxito"
        except sqlite3.IntegrityError:
            return False, "La placa o chasis ya existe."
        except Exception as e:
            return False, f"Error: {e}"
        finally:
            conn.close()

    @staticmethod
    def read_all():
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vehicles ORDER BY id DESC")
            return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def update(id_vehicle, model, plate, chassis, rate, is_available):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE vehicles 
                SET model=?, plate_number=?, chassis_number=?, daily_rate=?, is_available=?
                WHERE id=?
            """, (model, plate, chassis, rate, is_available, id_vehicle))
            conn.commit()
            return True, "Vehículo actualizado"
        except Exception as e:
            return False, f"Error al actualizar: {e}"
        finally:
            conn.close()

    @staticmethod
    def delete(id_vehicle):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vehicles WHERE id=?", (id_vehicle,))
            conn.commit()
            return True, "Vehículo eliminado"
        except sqlite3.IntegrityError:
            return False, "No se puede eliminar: Tiene rentas asociadas."
        finally:
            conn.close()
            