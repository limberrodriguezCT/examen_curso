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
           
            query = """
                SELECT u.id, u.user_name, u.password_hash, r.name as role_name 
                FROM users u
                JOIN roles r ON u.role_id = r.id
                WHERE u.user_name = ?
            """
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            
            if user:
                
                stored_hash = user['password_hash']
                
                
                if isinstance(stored_hash, str):
                    stored_hash = stored_hash.encode('utf-8')
                
                input_pass = password.encode('utf-8')
                
                if bcrypt.checkpw(input_pass, stored_hash):
                    return user 
            
            return None 
            
        except Exception as e:
            print(f"Error en login: {e}")
            return None
        finally:
            conn.close()