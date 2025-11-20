import sqlite3
import os
import bcrypt # Necesitamos bcrypt aquí para crear las claves

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'data', 'autopy.sqlite3')
SCHEMA_PATH = os.path.join(BASE_DIR, 'src', 'database', 'schema.sql')

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row 
    return conn

def seed_data(conn):
    """
    Esta función es tu 'DatabaseSeeder'. Crea los datos por defecto.
    """
    print("--- Ejecutando Semillas (Seeds) ---")
    cursor = conn.cursor()
    
    # 1. Roles (Ya estaban en el schema, pero aseguramos)
    cursor.execute("INSERT OR IGNORE INTO roles (id, name) VALUES (1, 'Administrador')")
    cursor.execute("INSERT OR IGNORE INTO roles (id, name) VALUES (2, 'Agente')")
    
    # 2. Usuarios por Defecto
    users_to_create = [
        (1, "admin", "admin123", 1),   # ID, user, pass, role_id
        (2, "agente", "agente123", 2)
    ]
    
    for uid, uname, upass, urole in users_to_create:
        # Verificamos si existe
        cursor.execute("SELECT id FROM users WHERE user_name = ?", (uname,))
        if not cursor.fetchone():
            # Si no existe, lo creamos
            print(f"   + Creando usuario: {uname}")
            # Hashing
            bytes_pass = upass.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(bytes_pass, salt)
            
            cursor.execute("""
                INSERT INTO users (id, user_name, password_hash, role_id)
                VALUES (?, ?, ?, ?)
            """, (uid, uname, hashed, urole))
        else:
            print(f"   . Usuario {uname} ya existe.")
            
    conn.commit()

def init_db():
    if not os.path.exists(SCHEMA_PATH):
        print(f"[ERROR] No existe el esquema en {SCHEMA_PATH}")
        return

    conn = get_connection()
    try:
        # 1. Migración (Crear tablas)
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
            
        # 2. Seeding (Datos iniciales) - LA MEJORA ESTÁ AQUÍ
        seed_data(conn)
        
        print(f"[OK] Base de datos lista en: {DB_PATH}")
    except Exception as e:
        print(f"[ERROR] BD: {e}")
    finally:
        conn.close()

# Permitir ejecutar este archivo solo para reiniciar la BD si se quiere
if __name__ == "__main__":
    init_db()