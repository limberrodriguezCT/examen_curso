from src.database.db import get_connection
import sqlite3

class RentalLogic:
    @staticmethod
    def get_available_vehicles():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, model, plate_number, daily_rate FROM vehicles WHERE is_available=1")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_customers():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name, document_number FROM customers")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def create_rental(customer_id, vehicle_id, days):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            # 1. Validar vehículo y obtener tarifa
            cursor.execute("SELECT daily_rate FROM vehicles WHERE id=?", (vehicle_id,))
            row = cursor.fetchone()
            if not row: return False, "Vehículo no encontrado"
            
            rate = row['daily_rate']
            total = rate * float(days)

            # 2. Insertar Renta (Forzamos int() para asegurar que el ID sea numérico)
            cursor.execute("""
                INSERT INTO rentals (customer_id, vehicle_id, total_amount, status)
                VALUES (?, ?, ?, 'Active')
            """, (int(customer_id), int(vehicle_id), total))

            # 3. Bloquear vehículo
            cursor.execute("UPDATE vehicles SET is_available=0 WHERE id=?", (vehicle_id,))
            
            conn.commit()
            return True, "Renta registrada correctamente"
        except Exception as e:
            conn.rollback()
            return False, f"Error BD: {e}"
        finally:
            conn.close()

    @staticmethod
    def read_all_active():
        conn = get_connection()
        cursor = conn.cursor()
        # --- SOLUCIÓN AQUÍ: Usamos AS para dar nombres únicos a las columnas ---
        query = """
            SELECT 
                r.id AS rental_id, 
                c.full_name AS cliente_nombre, 
                v.model AS vehiculo_modelo, 
                v.plate_number AS placa, 
                r.rental_date AS fecha, 
                r.total_amount AS total, 
                r.vehicle_id AS vid
            FROM rentals r
            JOIN customers c ON r.customer_id = c.id
            JOIN vehicles v ON r.vehicle_id = v.id
            WHERE r.status = 'Active'
            ORDER BY r.id DESC
        """
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def finalize_rental(rental_id, vehicle_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE rentals SET status='Completed', return_date=CURRENT_TIMESTAMP WHERE id=?", (rental_id,))
            cursor.execute("UPDATE vehicles SET is_available=1 WHERE id=?", (vehicle_id,))
            conn.commit()
            return True, "Vehículo devuelto."
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            conn.close()