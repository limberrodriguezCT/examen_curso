import bcrypt
import sqlite3
from src.database.db import get_connection

class AuthService:
    @staticmethod
    def login(username, password):
        """
        Verifica usuario y contraseña.
        Retorna el diccionario del usuario si es correcto, o None si falla.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            # Buscamos al usuario y traemos también el nombre de su ROL
            query = """
                SELECT u.id, u.user_name, u.password_hash, r.name as role_name 
                FROM users u
                JOIN roles r ON u.role_id = r.id
                WHERE u.user_name = ?
            """
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            
            if user:
                # Obtenemos el hash guardado en la BD
                stored_hash = user['password_hash']
                
                # Aseguramos que esté en bytes (necesario para bcrypt)
                if isinstance(stored_hash, str):
                    stored_hash = stored_hash.encode('utf-8')
                
                input_pass = password.encode('utf-8')
                
                # Comparamos la contraseña escrita con el hash
                if bcrypt.checkpw(input_pass, stored_hash):
                    return user # ¡Login exitoso!
            
            return None # Fallo
            
        except Exception as e:
            print(f"Error en login: {e}")
            return None
        finally:
            conn.close()