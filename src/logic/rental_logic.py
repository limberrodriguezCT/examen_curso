from src.database.db import get_connection
import sqlite3

class RentalLogic:
    @staticmethod
    def get_available_vehicles():
        """Trae solo vehículos disponibles (is_available=1)"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, model, plate_number, daily_rate FROM vehicles WHERE is_available=1")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_customers():
        """Trae todos los clientes"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name, document_number FROM customers")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def create_rental(customer_id, vehicle_id, days):
        """Crea la renta y bloquea el vehículo"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            # 1. Validar vehículo y obtener tarifa
            cursor.execute("SELECT daily_rate FROM vehicles WHERE id=?", (vehicle_id,))
            row = cursor.fetchone()
            if not row: return False, "Vehículo no encontrado"
            
            rate = row['daily_rate']
            total = rate * float(days)

            # 2. Insertar Renta (Forzamos int() para asegurar IDs numéricos)
            cursor.execute("""
                INSERT INTO rentals (customer_id, vehicle_id, total_amount, status)
                VALUES (?, ?, ?, 'Active')
            """, (int(customer_id), int(vehicle_id), total))

            # 3. Bloquear vehículo (Ponerlo en 0)
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
        """Trae todas las rentas activas con nombres en vez de IDs"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # USAMOS LEFT JOIN Y COALESCE PARA QUE NO FALLE SI BORRASTE UN CLIENTE
        query = """
            SELECT 
                r.id AS rental_id, 
                COALESCE(c.full_name, 'Cliente Eliminado') AS cliente_nombre, 
                COALESCE(v.model, 'Vehículo Eliminado') AS vehiculo_modelo, 
                COALESCE(v.plate_number, '---') AS placa, 
                r.rental_date AS fecha, 
                r.total_amount AS total, 
                r.vehicle_id AS vid
            FROM rentals r
            LEFT JOIN customers c ON r.customer_id = c.id
            LEFT JOIN vehicles v ON r.vehicle_id = v.id
            WHERE r.status = 'Active'
            ORDER BY r.id DESC
        """
        try:
            cursor.execute(query)
            data = cursor.fetchall()
            # Mensaje en consola para verificar si hay datos
            print(f"[DEBUG LOGIC] Se encontraron {len(data)} rentas activas en la BD.")
            return data
        except Exception as e:
            print(f"[ERROR LOGIC] Fallo en consulta: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def finalize_rental(rental_id, vehicle_id):
        """Termina la renta y libera el vehículo"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            # 1. Marcar renta como completada
            cursor.execute("UPDATE rentals SET status='Completed', return_date=CURRENT_TIMESTAMP WHERE id=?", (rental_id,))
            # 2. Liberar vehículo
            cursor.execute("UPDATE vehicles SET is_available=1 WHERE id=?", (vehicle_id,))
            conn.commit()
            return True, "Vehículo devuelto."
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            conn.close()