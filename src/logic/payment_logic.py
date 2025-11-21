from src.database.db import get_connection
import sqlite3

class PaymentLogic:
    @staticmethod
    def create_payment(rental_id, amount, currency="USD"):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO payments (rental_id, amount, currency, payment_date)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """, (rental_id, amount, currency))
            conn.commit()
            return True, "Pago registrado exitosamente."
        except Exception as e:
            return False, f"Error BD: {e}"
        finally:
            conn.close()

    @staticmethod
    def read_all():
        conn = get_connection()
        cursor = conn.cursor()
        # Consulta robusta: Si se borró el cliente o el auto, muestra "Desconocido" en vez de fallar
        query = """
            SELECT 
                p.id, 
                p.payment_date, 
                p.amount, 
                p.currency, 
                COALESCE(c.full_name, 'Cliente Eliminado') as cliente, 
                COALESCE(v.plate_number, '---') as placa,
                p.rental_id
            FROM payments p
            LEFT JOIN rentals r ON p.rental_id = r.id
            LEFT JOIN customers c ON r.customer_id = c.id
            LEFT JOIN vehicles v ON r.vehicle_id = v.id
            ORDER BY p.payment_date DESC
        """
        try:
            cursor.execute(query)
            data = cursor.fetchall()
            print(f"[DEBUG PAGOS] Se encontraron {len(data)} pagos en la base de datos.")
            return data
        except Exception as e:
            print(f"[ERROR PAGOS] Fallo consulta: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def update(payment_id, amount):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE payments SET amount=? WHERE id=?", (amount, payment_id))
            conn.commit()
            return True, "Pago actualizado."
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def delete(payment_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM payments WHERE id=?", (payment_id,))
            conn.commit()
            return True, "Pago eliminado."
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()