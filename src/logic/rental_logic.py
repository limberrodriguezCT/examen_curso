from src.database.db import get_connection
import sqlite3

class RentalLogic:
    @staticmethod
    def get_available_vehicles():
        """Trae solo los vehículos que están disponibles (is_available=1)"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, model, plate_number, daily_rate FROM vehicles WHERE is_available=1")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_customers():
        """Trae todos los clientes para el combobox"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name, document_number FROM customers")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def create_rental(customer_id, vehicle_id, days):
        """
        1. Crea la renta.
        2. Marca el vehículo como ocupado.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            # 1. Obtener tarifa del vehículo para calcular total
            cursor.execute("SELECT daily_rate FROM vehicles WHERE id=?", (vehicle_id,))
            row = cursor.fetchone()
            if not row: return False, "Vehículo no encontrado"
            
            rate = row['daily_rate']
            total = rate * float(days)

            # 2. Insertar Renta
            cursor.execute("""
                INSERT INTO rentals (customer_id, vehicle_id, total_amount, status)
                VALUES (?, ?, ?, 'Active')
            """, (customer_id, vehicle_id, total))

            # 3. Actualizar Vehículo a NO DISPONIBLE (0)
            cursor.execute("UPDATE vehicles SET is_available=0 WHERE id=?", (vehicle_id,))
            
            conn.commit()
            return True, "Renta registrada con éxito"
        except Exception as e:
            conn.rollback() # Si falla, deshace todo
            return False, f"Error: {e}"
        finally:
            conn.close()

    @staticmethod
    def read_all_active():
        conn = get_connection()
        cursor = conn.cursor()
        # Hacemos JOIN para mostrar nombres en vez de IDs
        query = """
            SELECT r.id, c.full_name, v.model, v.plate_number, r.rental_date, r.total_amount, r.status, r.vehicle_id
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
        """
        Termina la renta y libera el vehículo.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            # 1. Marcar renta como completada
            cursor.execute("UPDATE rentals SET status='Completed', return_date=CURRENT_TIMESTAMP WHERE id=?", (rental_id,))
            
            # 2. Liberar vehículo (Disponible)
            cursor.execute("UPDATE vehicles SET is_available=1 WHERE id=?", (vehicle_id,))
            
            conn.commit()
            return True, "Vehículo devuelto y renta finalizada."
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            conn.close()