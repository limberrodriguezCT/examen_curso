import sqlite3
import os

# 1. Definimos las rutas exactas para que Windows no se pierda
# Esto busca la carpeta raíz del proyecto automáticamente
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Ruta donde se guardará la base de datos (carpeta 'data')
DB_PATH = os.path.join(BASE_DIR, 'data', 'autopy.sqlite3')

# Ruta donde está el script SQL para crear las tablas
SCHEMA_PATH = os.path.join(BASE_DIR, 'src', 'database', 'schema.sql')

def get_connection():
    """
    Retorna la conexión a la base de datos.
    Si la carpeta 'data' no existe, la crea.
    """
    # Crear carpeta data si no existe
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    # Activar llaves foráneas (FOREIGN KEYS)
    conn.execute("PRAGMA foreign_keys = ON")
    # Permitir acceder a columnas por nombre (ej: row['id'])
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    """
    Busca el archivo schema.sql y ejecuta los comandos para crear las tablas.
    Esta es la función que tu main.py está buscando.
    """
    if not os.path.exists(SCHEMA_PATH):
        print(f"[ERROR CRÍTICO] No se encontró el esquema en: {SCHEMA_PATH}")
        print("Verifica que hayas creado el archivo src/database/schema.sql")
        return

    conn = get_connection()
    try:
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            conn.executescript(sql_script)
            print(f"[OK] Base de datos verificada/creada en: {DB_PATH}")
            
            # --- Verificación rápida ---
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM roles")
            count = cursor.fetchone()[0]
            print(f"[INFO] Roles existentes: {count}")
            
    except Exception as e:
        print(f"[ERROR] Fallo al inicializar la BD: {e}")
    finally:
        conn.close()