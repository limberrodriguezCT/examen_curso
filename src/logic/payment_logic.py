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
            return True, "Pago registrado."
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def read_all():
        conn = get_connection()
        cursor = conn.cursor()
        # Mostramos info de la renta y el cliente asociado al pago
        query = """
            SELECT p.id, p.payment_date, p.amount, p.currency, c.full_name, v.plate_number
            FROM payments p
            JOIN rentals r ON p.rental_id = r.id
            JOIN customers c ON r.customer_id = c.id
            JOIN vehicles v ON r.vehicle_id = v.id
            ORDER BY p.payment_date DESC
        """
        data = cursor.fetchall()
        conn.close()
        return data