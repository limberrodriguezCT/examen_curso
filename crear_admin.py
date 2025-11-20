import sqlite3
import bcrypt
# Importamos init_db para asegurar que las tablas existan
from src.database.db import get_connection, init_db 

def create_admin_user():
    # 1. PRIMER PASO CRÍTICO: Crear las tablas si no existen
    print("--- Verificando estructura de la base de datos ---")
    init_db() 
    
    print("\n--- Creando usuario Administrador ---")
    conn = get_connection()
    cursor = conn.cursor()
    
    # 2. Datos del usuario
    username = "admin"
    password_raw = "admin123"
    
    # 3. Encriptar contraseña
    print(f"Encriptando contraseña...")
    bytes_password = password_raw.encode('utf-8')
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(bytes_password, salt)
    
    try:
        # 4. Asegurar que existan los roles (por si init_db no los insertó)
        cursor.execute("INSERT OR IGNORE INTO roles (id, name) VALUES (1, 'Administrador')")
        cursor.execute("INSERT OR IGNORE INTO roles (id, name) VALUES (2, 'Agente')")
        
        # 5. Insertar el usuario
        cursor.execute("""
            INSERT INTO users (user_name, password_hash, role_id)
            VALUES (?, ?, ?)
        """, (username, password_hash, 1))
        
        conn.commit()
        print(f"✅ ¡ÉXITO! Usuario '{username}' creado correctamente.")
        
    except sqlite3.IntegrityError:
        print(f"⚠️ El usuario '{username}' YA EXISTE. No es necesario crearlo de nuevo.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_admin_user()